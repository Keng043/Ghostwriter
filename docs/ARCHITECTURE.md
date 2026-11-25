# Architecture

## Design boundaries

Ghostwriter separates model reasoning from local data management.

- The **Agent** and **Skill** define how an LLM calibrates style, audits briefs, drafts content, and learns from corrections.
- The **Python core** validates profile data, stores it locally, imports/exports JSON, checks required brief fields, and assembles provider-neutral prompts.
- The **profile schema** is the portable contract between tools and model providers.

## Data flow

1. A user provides writing samples during calibration.
2. The model analyzes observable patterns and asks the user to confirm the proposed Style DNA.
3. The profile manager stores the confirmed compact profile.
4. During drafting, the agent loads only the active user's profile and the current brief.
5. The auditor blocks drafting when required facts are missing or explicitly conflicting.
6. The writer generates a draft; the agent checks it against the brief.
7. User corrections update only the relevant profile dimension when treated as a standing preference.

## Storage and identity

Profiles are separate JSON files keyed by a sanitized user ID. The CLI defaults to the operating system's user data directory. The profile store is local-only and does not implement synchronization, authentication, or encryption. A shared multi-user server would require a separate authenticated backend and access-control review.

## Deliberate limitations in v0.1

- Style inference requires an AI model using the included Agent/Skill instructions; the Python package does not pretend to infer style from heuristics.
- No LLM provider is hard-coded.
- No cloud memory or telemetry is included.
- Profile export is plain JSON and must be handled as private data.
