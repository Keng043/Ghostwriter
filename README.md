# Ghostwriter

**Personal Writing Agent + portable Skill**

Ghostwriter learns a user's preferred writing style, keeps a portable Style DNA profile, checks source information before drafting, and creates writing in the user's preferred voice. It is provider-neutral: the Skill contains the reasoning workflow, while the Python package manages local profiles and validation.

## What is included

- **Agent instructions** in `agent/` for system-level behavior and workflow.
- **Installable Skill** in `skills/ghostwriter/` with calibration, audit, drafting, and correction guidance.
- **Local profile manager** in `src/ghostwriter/` (Python 3.10+, standard library only).
- **Eight-dimension Style DNA** with JSON import/export.
- **Strict data audit** that flags missing required fields and explicit conflicts.
- **Privacy-first defaults**: raw writing samples are not retained unless the user opts in.

## Quick start

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
ghostwriter init --id my-profile --name "My Writing Profile" --language th
ghostwriter show my-profile
```

If the `ghostwriter` command is not on PATH, use:

```powershell
python -m ghostwriter.cli init --id my-profile --name "My Writing Profile" --language th
```

## Use the Skill

Copy `skills/ghostwriter/` into the skills directory supported by your AI agent, or provide `SKILL.md` as the agent's skill/instruction file. Read [Skill installation](docs/INSTALLATION.md) for platform-neutral setup. Load the user's profile JSON as private context when the agent supports local files.

## Profile commands

```powershell
ghostwriter init --id writer-a --name "Writer A" --language th
ghostwriter list
ghostwriter show writer-a
ghostwriter export writer-a .\writer-a-profile.json
ghostwriter import .\writer-a-profile.json
ghostwriter audit .\brief.json --required recipient purpose deadline
ghostwriter prompt writer-a .\brief.txt
```

The `prompt` command prints a provider-neutral drafting prompt. Paste it into the AI model or agent you use. Ghostwriter does not call a paid model API or transmit profile data.

## Privacy and security

- Profiles are stored locally in the operating system's user data directory by default.
- Windows: `%LOCALAPPDATA%\Ghostwriter\profiles`.
- macOS/Linux: `~/.local/share/ghostwriter/profiles` (or `$XDG_DATA_HOME/ghostwriter/profiles`).
- Raw samples are excluded from storage by default. Explicitly set `retain_samples: true` only after obtaining consent.
- Never commit personal profiles, raw samples, credentials, API keys, or private drafts. The repository ignores local storage directories and profile/sample files.
- Exported profile JSON is personal data. Store and share it deliberately.

## Development

```powershell
python -m unittest discover -s tests -v
python -m compileall src
```

## Current scope and limitations

The Python package stores and validates profiles; it does not independently infer writing style. Style analysis and natural-language drafting are performed by the AI Agent/Skill using the calibration instructions. A model provider can be connected later without changing the profile format. Local JSON files are not encrypted by this package; use OS disk encryption and protect exported files.

## License

MIT. See [LICENSE](LICENSE).
