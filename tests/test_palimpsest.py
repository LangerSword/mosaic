import json
import tempfile
import unittest
from pathlib import Path

from mosaic_audit import audit_source
from mosaic_forge import KINDS
from mosaic_tools import TOOL_SPECS, h_audit, h_components, h_forge, h_index, h_invent, h_recipe, h_stacks


class IndexTests(unittest.TestCase):
    def test_index_has_ten_families(self):
        out = json.loads(h_index({}))
        self.assertTrue(out["ok"])
        self.assertEqual(len(out["families"]), 10)
        self.assertIn("paper-ink", [f["id"] for f in out["families"]])

    def test_tool_specs_are_named(self):
        self.assertEqual([s["name"] for s in TOOL_SPECS],
                         ["mosaic_index", "mosaic_components", "mosaic_stacks", "mosaic_forge",
                          "mosaic_invent", "mosaic_recipe", "mosaic_audit"])

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
        self.assertEqual(len(out["kinds"]), 7)


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
