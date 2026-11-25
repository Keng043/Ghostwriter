# Installation

## Python package

Requires Python 3.10 or newer. From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
ghostwriter init --id my-profile --name "My Profile" --language th
```

macOS/Linux:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
ghostwriter init --id my-profile --name "My Profile" --language en
```

## Agent instructions

Add the contents of `agent/` to the system/developer instruction area of the agent platform you use. Keep the rules and workflow together.

## Skill package

Copy the entire `skills/ghostwriter/` directory to the Skill directory supported by your agent platform. If the platform expects a single skill file, provide `SKILL.md` and keep the `references/` folder adjacent so relative links remain available.

Different agent platforms use different skill discovery conventions. This repository does not claim automatic installation into every provider.

## Profile portability

Export with `ghostwriter export my-profile ./my-profile.json`. Import on another device with `ghostwriter import ./my-profile.json`. Treat the exported file as private data.
