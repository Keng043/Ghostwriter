# Privacy Model

Ghostwriter is local-first by design.

- The CLI stores profiles on the current machine.
- The default profile contains style preferences, not raw writing samples.
- Raw samples are rejected unless `retain_samples` is explicitly enabled.
- The drafting prompt intentionally omits raw sample text.
- No telemetry, analytics, cloud sync, or model API calls are implemented in this package.
- AI providers may process prompts according to their own terms when a user chooses to send a brief/profile to them. Review provider privacy settings before use.
- JSON profile exports are not encrypted. Protect them like personal documents.
- Public repository content must contain generic examples only.

Users can delete a profile by deleting its JSON file from the local profiles directory.
