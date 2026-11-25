import json
import tempfile
import unittest
from pathlib import Path

from ghostwriter.auditor import audit_brief, build_clarification_questions
from ghostwriter.models import StyleProfile
from ghostwriter.storage import ProfileStore
from ghostwriter.prompts import drafting_prompt

class GhostwriterCoreTests(unittest.TestCase):
    def test_profile_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            store = ProfileStore(Path(folder))
            profile = StyleProfile(user_id="writer-1", style_dna={"tone": "semi-formal"})
            store.save(profile)
            loaded = store.load("writer-1")
            self.assertEqual(loaded.style_dna["tone"], "semi-formal")

    def test_raw_samples_require_opt_in(self):
        profile = StyleProfile(user_id="writer", samples=["private text"])
        with self.assertRaises(ValueError):
            profile.validate()

    def test_audit_missing_fields(self):
        result = audit_brief({"purpose": "weekly report"}, ("purpose", "period"))
        self.assertFalse(result.complete)
        self.assertEqual(result.missing, ["period"])
        self.assertEqual(len(build_clarification_questions(result)), 1)

    def test_conflict_blocks_completion(self):
        result = audit_brief({"period": {"conflict": True, "description": "Two dates"}})
        self.assertFalse(result.complete)
        self.assertEqual(result.conflicts, ["Two dates"])

    def test_prompt_excludes_sample_text(self):
        profile = StyleProfile(user_id="writer", retain_samples=True, samples=["private sample"])
        prompt = drafting_prompt(profile, "Write a short update")
        self.assertNotIn("private sample", prompt)
        self.assertIn("Never invent", prompt)

if __name__ == "__main__":
    unittest.main()
