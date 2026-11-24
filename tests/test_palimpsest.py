import json
import tempfile
import unittest
from pathlib import Path

from mosaic_audit import audit_source
from mosaic_tools import TOOL_SPECS, h_audit, h_components, h_index, h_recipe


class IndexTests(unittest.TestCase):
    def test_index_has_ten_families(self):
        out = json.loads(h_index({}))
        self.assertTrue(out["ok"])
        self.assertEqual(len(out["families"]), 10)
        self.assertIn("paper-ink", [f["id"] for f in out["families"]])

    def test_tool_specs_are_named(self):
        self.assertEqual([s["name"] for s in TOOL_SPECS],
                         ["mosaic_index", "mosaic_components", "mosaic_recipe", "mosaic_audit"])

    def test_components_filter(self):
        out = json.loads(h_components({"family": "press"}))
        self.assertTrue(out["ok"])
        self.assertGreater(out["count"], 3)
        self.assertTrue(all(c["family"] == "press" for c in out["components"]))
        self.assertIn("hold-to-confirm", [c["id"] for c in out["components"]])


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
