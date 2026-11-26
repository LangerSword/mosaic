"""Mosaic: design direction for Hermes.

The plugin is deliberately small: an index of reference families, a
deterministic recipe builder and a local source audit. It does not render,
fetch, execute or publish anything.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

__version__ = "0.6.0"
TOOLSET = "mosaic"


def register(ctx) -> None:
    from .mosaic_tools import TOOL_SPECS

    for spec in TOOL_SPECS:
        def tool_handler(args: dict, _run=spec["handler"], **_kw) -> str:
            return _run(args or {})

        ctx.register_tool(
            name=spec["name"],
            toolset=TOOLSET,
            schema=spec["schema"],
            handler=tool_handler,
            description=spec["description"],
            emoji=spec.get("emoji", "🎛️"),
        )


__all__ = ["register", "__version__"]
