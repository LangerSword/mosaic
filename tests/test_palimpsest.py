import json
import tempfile
import unittest
from pathlib import Path

from mosaic_audit import audit_source
from mosaic_data import MOODS
from mosaic_design import _tokens
from mosaic_forge import KINDS
from mosaic_tools import (TOOL_SPECS, h_audit, h_components, h_critique, h_design, h_forge,
                         h_index, h_invent, h_recipe, h_score, h_stacks, h_study, h_visual)
from mosaic_visual import _target


class IndexTests(unittest.TestCase):
    def test_index_has_thirteen_families(self):
        out = json.loads(h_index({}))
        self.assertTrue(out["ok"])
        self.assertEqual(len(out["families"]), 13)
        self.assertIn("paper-ink", [f["id"] for f in out["families"]])
        self.assertEqual(len(out["methods"]), 5)

    def test_tool_specs_are_named(self):
        self.assertEqual([s["name"] for s in TOOL_SPECS],
                         ["mosaic_index", "mosaic_study", "mosaic_design", "mosaic_components",
                          "mosaic_stacks", "mosaic_forge", "mosaic_invent", "mosaic_recipe",
                          "mosaic_visual", "mosaic_audit", "mosaic_critique", "mosaic_score"])

    def test_components_filter(self):
        out = json.loads(h_components({"family": "press"}))
        self.assertTrue(out["ok"])
        self.assertGreater(out["count"], 3)
        self.assertTrue(all(c["family"] == "press" for c in out["components"]))
        self.assertIn("hold-to-confirm", [c["id"] for c in out["components"]])


class ForgeTests(unittest.TestCase):
    def test_forge_emits_distinct_files_for_all_stacks(self):
        out = json.loads(h_forge({"kind": "swipe-confirm", "stack": "all", "motion": "gsap"}))
        self.assertTrue(out["ok"])
        paths = [f["path"] for f in out["files"]]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertIn("swipe-confirm.js", paths)
        self.assertIn("index.svelte", paths)
        self.assertIn("index.vue", paths)
        self.assertIn("index.astro", paths)
        self.assertIn("gsap", out["deps"])

    def test_forge_has_no_unresolved_placeholders(self):
        out = json.loads(h_forge({"kind": "paper-plane", "stack": "next", "motion": "gsap"}))
        core = next(f["content"] for f in out["files"] if f["path"].endswith(".js"))
        self.assertIn("customElements.define('mosaic-paper-plane'", core)
        self.assertNotIn("{tag}", core)
        self.assertNotIn("{{", core)
        self.assertIn('"use client"', next(f["content"] for f in out["files"] if f["path"] == "index.tsx"))

    def test_forge_rejects_unknown_target(self):
        with self.assertRaises(ValueError):
            h_forge({"kind": "hold", "stack": "angular"})

    def test_stacks_are_indexed(self):
        out = json.loads(h_stacks({}))
        self.assertTrue(out["ok"])
        self.assertEqual(len(out["stacks"]), 6)
        self.assertEqual(len(out["kinds"]), 11)


class InventTests(unittest.TestCase):
    def test_invent_is_deterministic_and_unique(self):
        args = {"brief": "A quiet onboarding for a design tool", "count": 3, "seed": 7}
        one = json.loads(h_invent(args))
        two = json.loads(h_invent(args))
        self.assertEqual(one, two)
        self.assertEqual(len(one["candidates"]), 3)
        self.assertEqual(len({c["id"] for c in one["candidates"]}), 3)
        self.assertEqual(len({c["input"] for c in one["candidates"]}), 3)

    def test_invent_scores_and_forge_kind(self):
        out = json.loads(h_invent({"brief": "A banking app where a transfer feels deliberate", "count": 3}))
        for candidate in out["candidates"]:
            self.assertEqual(set(candidate["scores"]), {"coherence", "legibility", "novelty", "restraint", "fit"})
            self.assertGreaterEqual(candidate["overall"], 0)
            self.assertLessEqual(candidate["overall"], 10)
            self.assertIn(candidate["forge_kind"], KINDS)

    def test_invent_respects_no_hover(self):
        out = json.loads(h_invent({"brief": "A quiet keyboard-first archive", "constraints": "no hover", "count": 3}))
        self.assertTrue(all(c["input"] != "hover" for c in out["candidates"]))

    def test_invent_rejects_short_brief(self):
        with self.assertRaises(ValueError):
            h_invent({"brief": "short"})


class RecipeTests(unittest.TestCase):
    def test_card_brief_picks_cards(self):
        out = json.loads(h_recipe({"brief": "A collectible card deck for a racing game"}))
        self.assertTrue(out["ok"])
        self.assertIn("cards", [m["id"] for m in out["signature_moves"]])
        self.assertIn("--paper", out["tokens"])
        self.assertIn("--display", out["tokens"])
        self.assertIn("face-card", out["component_candidates"])

    def test_agent_brief_picks_loading(self):
        out = json.loads(h_recipe({"brief": "An agent that streams its work while it reads files"}))
        self.assertIn("loading", [m["id"] for m in out["signature_moves"]])

    def test_recipe_is_deterministic(self):
        args = {"brief": "A quiet portfolio for a type designer", "mood": "editorial"}
        self.assertEqual(h_recipe(args), h_recipe(args))

    def test_bad_mood_is_rejected(self):
        with self.assertRaises(ValueError):
            h_recipe({"brief": "A page", "mood": "loud"})

    def test_recipe_has_two_distinct_moves(self):
        out = json.loads(h_recipe({"brief": "A collectible deck for a racing game", "mood": "tactile"}))
        ids = [m["id"] for m in out["signature_moves"]]
        self.assertEqual(len(ids), 2)
        self.assertEqual(len(set(ids)), 2)

    def test_recipe_has_verification(self):
        out = json.loads(h_recipe({"brief": "A tactile pricing page"}))
        self.assertGreaterEqual(len(out["acceptance"]), 6)
        self.assertIn("reduced", " ".join(out["acceptance"]).lower())


class DesignTests(unittest.TestCase):
    brief = "A quiet portfolio for a type designer who needs clients to trust the process"

    def test_design_proposes_distinct_concepts_and_chooses_one(self):
        out = json.loads(h_design({"brief": self.brief}))
        self.assertTrue(out["ok"])
        self.assertEqual(len(out["concepts"]), 3)
        self.assertEqual(len({c["id"] for c in out["concepts"]}), 3)
        self.assertIn(out["chosen"]["id"], {c["id"] for c in out["concepts"]})
        self.assertGreaterEqual(out["chosen"]["scores"]["overall"], 7)
        self.assertIn("--field", out["system"]["tokens"])
        self.assertIn("ink_on_field", out["system"]["contrast"])

    def test_design_is_deterministic(self):
        args = {"brief": self.brief, "audience": "independent studio founders", "seed": 12}
        self.assertEqual(h_design(args), h_design(args))

    def test_reference_observations_are_required_for_principles(self):
        bare = json.loads(h_study({"reference": "https://example.com/reference"}))
        self.assertEqual(bare["status"], "needs_observations")
        self.assertEqual(bare["confidence"], "low")
        studied = json.loads(h_study({
            "reference": {
                "name": "DIA",
                "observations": {
                    "layout": "index and specimen split",
                    "what_works": "the index is the navigation",
                },
            }
        }))
        self.assertEqual(studied["status"], "studied")
        self.assertTrue(studied["principles"])

    def test_page_mode_emits_a_content_contract_not_unresolved_tokens(self):
        out = json.loads(h_design({"brief": self.brief, "mode": "page"}))
        page = out["page"]["files"][0]
        self.assertEqual(page["path"], "index.html")
        self.assertNotIn("{{", page["content"])
        self.assertIn("data-slot", page["content"])
        self.assertIn("--field", page["content"])
        self.assertIn("layout-", page["content"])
        self.assertIn("prefers-reduced-motion", page["content"])

    def test_tokens_meet_text_contrast_for_every_mood(self):
        for mood in MOODS:
            contrast = _tokens(mood, {})["--contrast"]
            self.assertGreaterEqual(contrast["ink_on_field"], 4.5, mood)
            self.assertGreaterEqual(contrast["signal_on_field"], 4.5, mood)
            self.assertGreaterEqual(contrast["signal_on_surface"], 4.5, mood)
            self.assertGreaterEqual(contrast["muted_on_field"], 4.5, mood)

    def test_design_rejects_bad_inputs(self):
        with self.assertRaises(ValueError):
            h_design({"brief": "short"})
        with self.assertRaises(ValueError):
            h_design({"brief": self.brief, "mode": "magic"})
        with self.assertRaises(ValueError):
            h_design({"brief": self.brief, "mood": "loud"})


class CritiqueTests(unittest.TestCase):
    def test_critique_flags_generic_copy_and_missing_focus(self):
        source = "<html><body><h1>We unlock seamless growth</h1><button>Start</button></body></html>"
        out = json.loads(h_critique({"source": source}))
        self.assertTrue(out["ok"])
        rules = {f["rule"] for f in out["findings"]}
        self.assertIn("generic-copy", rules)
        self.assertIn("no-focus-visible", rules)
        self.assertIn(out["verdict"], {"revise", "reject"})

    def test_critique_passes_the_generated_page(self):
        page = json.loads(h_design({"brief": DesignTests.brief, "mode": "page"}))["page"]["files"][0]["content"]
        out = json.loads(h_critique({"source": page}))
        self.assertEqual(out["verdict"], "pass")
        self.assertNotIn("no-slot-contract", {f["rule"] for f in out["findings"]})


class MaterialTests(unittest.TestCase):
    def test_index_exposes_ascii_and_glass(self):
        out = json.loads(h_index({}))
        ids = {family["id"] for family in out["families"]}
        self.assertIn("ascii", ids)
        self.assertIn("glass", ids)

    def test_ascii_forge_is_interactive_and_has_fallback(self):
        out = json.loads(h_forge({"kind": "ascii-field", "stack": "html", "motion": "css"}))
        js = next(f["content"] for f in out["files"] if f["path"].endswith(".js"))
        self.assertIn("mosaic-ascii-field", js)
        self.assertIn("requestAnimationFrame", js)
        self.assertIn("prefers-reduced-motion", js)
        self.assertIn("IntersectionObserver", js)

    def test_glass_forge_has_a_real_fallback(self):
        out = json.loads(h_forge({"kind": "glass-stack", "stack": "html", "motion": "css"}))
        js = next(f["content"] for f in out["files"] if f["path"].endswith(".js"))
        self.assertIn("backdrop-filter", js)
        self.assertIn("@supports not (backdrop-filter", js)
        self.assertIn("aria-pressed", js)

    def test_new_kinds_keep_pointer_and_reduced_motion_fallbacks(self):
        for kind, tag in (("magnetic-link", "mosaic-magnetic-link"), ("cursor-lens", "mosaic-cursor-lens")):
            out = json.loads(h_forge({"kind": kind, "stack": "html", "motion": "css"}))
            js = next(f["content"] for f in out["files"] if f["path"].endswith(".js"))
            self.assertIn(f"customElements.define('{tag}'", js)
            self.assertIn("prefers-reduced-motion", js)

    def test_download_ring_uses_a_full_circle(self):
        out = json.loads(h_forge({"kind": "download-ring", "stack": "html", "motion": "css"}))
        js = next(f["content"] for f in out["files"] if f["path"].endswith(".js"))
        self.assertIn("calc(var(--p) * 360deg)", js)
        self.assertNotIn("calc(var(--p) * 3.6deg)", js)


class VisualTests(unittest.TestCase):
    def test_target_accepts_a_local_html_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "page.html"
            path.write_text("<h1>Read the room.</h1>", encoding="utf-8")
            url, label = _target(str(path))
            self.assertTrue(url.startswith("file://"))
            self.assertEqual(label, str(path.resolve()))

    def test_target_rejects_non_html(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "notes.txt"
            path.write_text("not a page", encoding="utf-8")
            with self.assertRaises(ValueError):
                _target(str(path))

    def test_visual_requires_one_input(self):
        with self.assertRaises(ValueError):
            h_visual({})
        with self.assertRaises(ValueError):
            h_visual({"target": "https://example.com", "source": "<h1>x</h1>"})


class ScoreTests(unittest.TestCase):
    def test_score_passes_a_strong_generated_page(self):
        page = json.loads(h_design({"brief": DesignTests.brief, "mode": "page"}))["page"]["files"][0]["content"]
        out = json.loads(h_score({"source": page, "brief": DesignTests.brief}))
        self.assertTrue(out["ok"])
        self.assertGreaterEqual(out["overall"], 8.0)
        self.assertIn(out["verdict"], {"ship", "revise"})
        self.assertFalse(out["blockers"])

    def test_score_rejects_generic_copy_and_missing_states(self):
        source = "<html><body><h1>We unlock seamless growth</h1><button>Start</button></body></html>"
        out = json.loads(h_score({"source": source, "brief": "A quiet archive"}))
        self.assertLess(out["overall"], 8)
        self.assertIn(out["verdict"], {"revise", "reject"})
        self.assertIn("No focus-visible path.", out["blockers"])

    def test_score_accepts_a_path(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "page.html"
            path.write_text("<h1>Read the room.</h1><p data-slot=\"body\">One real note.</p>", encoding="utf-8")
            out = json.loads(h_score({"path": str(path), "brief": "An archive"}))
            self.assertTrue(out["ok"])
            self.assertIn("scores", out)


class AuditTests(unittest.TestCase):
    def test_clean_source_has_no_findings(self):
        out = json.loads(h_audit({"source": "body { color: #17181a; }"}))
        self.assertTrue(out["ok"])
        self.assertEqual(out["finding_count"], 0)

    def test_generic_patterns_are_flagged(self):
        src = """
        .x { transition: all 200ms ease; font-family: Inter, sans-serif; }
        .y { background: linear-gradient(135deg, #667eea, #764ba2); }
        .z { backdrop-filter: blur(20px); }
        """
        out = json.loads(h_audit({"source": src}))
        rules = {f["rule"] for f in out["findings"]}
        self.assertIn("transition-all", rules)
        self.assertIn("generic-inter", rules)
        self.assertIn("purple-gradient", rules)
        self.assertIn("glass-overload", rules)
        self.assertIn("no-reduced-motion", rules)
        self.assertLess(out["score"], 100)

    def test_path_read_and_missing_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a.css"
            p.write_text(".a { transition: all 1s; }\n", encoding="utf-8")
            out = json.loads(h_audit({"path": str(p)}))
            self.assertTrue(out["ok"])
            self.assertEqual(out["findings"][0]["rule"], "transition-all")
        missing = json.loads(h_audit({"path": str(Path(d) / "nope.css")}))
        self.assertFalse(missing["ok"])

    def test_audit_requires_one_input(self):
        with self.assertRaises(ValueError):
            h_audit({})
        with self.assertRaises(ValueError):
            h_audit({"path": "a.css", "source": "body{}"})


if __name__ == "__main__":
    unittest.main()
