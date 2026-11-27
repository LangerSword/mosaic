"""Mosaic Visual: a measured browser gate, not an opinion.

The handler is deliberately small. It resolves a page target, locates a Python
that can import Playwright, runs ``mosaic_visual_runner.py`` once, and returns
the runner's compact JSON plus screenshot paths. The first run on a machine
without a browser returns a structured ``needs_browser`` result instead of a
green visual claim.

Efficient use:
- one browser launch, two viewports (1440x900 and 390x844)
- no screenshots inline in the tool result
- no model call; all gates are deterministic DOM and pixel measurements
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

RUNNER = Path(__file__).with_name("mosaic_visual_runner.py")
MAX_TIMEOUT = 75


def _data_root() -> Path:
    override = os.environ.get("HERMES_PLUGIN_DATA")
    if override:
        return Path(override).expanduser() / "mosaic" / "visual"
    return Path.home() / ".hermes" / "plugin-data" / "mosaic" / "visual"


def _python_with_playwright() -> str | None:
    candidates = [
        os.environ.get("MOSAIC_BROWSER_PYTHON"),
        str(Path.home() / ".venv" / "bin" / "python"),
        sys.executable,
        shutil.which("python3"),
    ]
    seen = set()
    for candidate in candidates:
        if not candidate or candidate in seen or not Path(candidate).is_file():
            continue
        seen.add(candidate)
        try:
            probe = subprocess.run(
                [candidate, "-c", "import playwright.sync_api; print('ok')"],
                capture_output=True,
                text=True,
                timeout=8,
                env=_child_env(),
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if probe.returncode == 0 and "ok" in probe.stdout:
            return candidate
    return None


def _child_env() -> dict[str, str]:
    keep = {"PATH", "HOME", "USER", "LOGNAME", "LANG", "LC_ALL", "LC_CTYPE", "TMPDIR",
            "TZ", "XDG_RUNTIME_DIR", "DISPLAY", "WAYLAND_DISPLAY"}
    return {key: value for key, value in os.environ.items() if key in keep}


def _target(target: str) -> tuple[str, str]:
    if not isinstance(target, str) or not target.strip():
        raise ValueError("target must be a URL or a local .html file")
    target = target.strip()
    if target.startswith(("http://", "https://")):
        return target, target
    path = Path(target).expanduser().resolve()
    if path.is_dir():
        path = path / "index.html"
    if not path.is_file():
        raise ValueError(f"not a local file: {path}")
    if path.suffix.lower() not in {".html", ".htm"}:
        raise ValueError("local visual targets must be .html or .htm")
    return path.as_uri(), str(path)


def visual(target: str, *, out_dir: str | None = None) -> dict:
    url, label = _target(target)
    python = _python_with_playwright()
    if not python:
        return {
            "ok": False,
            "status": "needs_browser",
            "target": label,
            "error": "No Python with Playwright was found.",
            "fix": "Install Playwright Chromium in a local venv and set MOSAIC_BROWSER_PYTHON to that interpreter.",
        }
    if out_dir:
        out = Path(out_dir).expanduser().resolve()
    else:
        digest = hashlib.sha256(label.encode()).hexdigest()[:12]
        out = _data_root() / digest
    out.mkdir(parents=True, exist_ok=True)
    try:
        proc = subprocess.run(
            [python, str(RUNNER), "--url", url, "--out", str(out)],
            capture_output=True,
            text=True,
            timeout=MAX_TIMEOUT,
            env=_child_env(),
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "status": "timeout", "target": label,
                "error": f"visual render exceeded {MAX_TIMEOUT}s"}
    if proc.returncode != 0 and not proc.stdout.strip():
        return {"ok": False, "status": "render_failed", "target": label,
                "error": (proc.stderr or "runner returned no JSON")[-1200:]}
    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "status": "bad_runner_output", "target": label,
                "error": (proc.stderr or proc.stdout)[-1200:]}
    report["target"] = label
    canonical = {
        "target": label,
        "checks": report.get("checks", []),
        "viewports": [
            {
                "name": view.get("name"),
                "width": view.get("width"),
                "height": view.get("height"),
                "blockers": view.get("blockers", []),
                "image": view.get("image", {}),
                "text_count": view.get("text_count"),
                "focus_visible": view.get("focus_visible"),
            }
            for view in report.get("viewports", [])
        ],
        "blockers": report.get("blockers", []),
    }
    report["evidence_id"] = "v1-" + hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:16]
    report["renderer"] = python
    report["output_dir"] = str(out)
    return report


def visual_source(source: str, *, name: str = "source.html") -> dict:
    """Write a source string to a temp page and run the visual gate."""
    import tempfile
    root = Path(tempfile.mkdtemp(prefix="mosaic-visual-"))
    path = root / name
    path.write_text(source, encoding="utf-8")
    return visual(str(path), out_dir=str(root / "shots"))