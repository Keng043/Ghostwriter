"""Command-line tools for local Ghostwriter profile management."""
import argparse
import json
from pathlib import Path
from . import __version__
from .auditor import audit_brief
from .models import StyleProfile
from .prompts import drafting_prompt
from .storage import ProfileStore

def main() -> None:
    parser = argparse.ArgumentParser(prog="ghostwriter", description="Personal writing-style profile manager")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--data-dir", type=Path, help="Override local profile directory")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="Create a new local profile")
    init.add_argument("--id", required=True)
    init.add_argument("--name", default="Writer")
    init.add_argument("--language", default="en")
    show = sub.add_parser("show", help="Show a profile")
    show.add_argument("id")
    sub.add_parser("list", help="List local profile IDs")
    export = sub.add_parser("export", help="Export a profile as JSON")
    export.add_argument("id")
    export.add_argument("destination", type=Path)
    imp = sub.add_parser("import", help="Import a profile JSON")
    imp.add_argument("source", type=Path)
    audit = sub.add_parser("audit", help="Check required fields in a JSON brief")
    audit.add_argument("source", type=Path)
    audit.add_argument("--required", nargs="*", default=[])
    prompt = sub.add_parser("prompt", help="Create a provider-neutral drafting prompt")
    prompt.add_argument("id")
    prompt.add_argument("brief", type=Path)
    args = parser.parse_args()
    store = ProfileStore(args.data_dir)
    if args.command == "init":
        path = store.save(StyleProfile(user_id=args.id, display_name=args.name, language=args.language))
        print(f"Created profile: {path}")
    elif args.command == "show":
        print(json.dumps(store.load(args.id).to_dict(), ensure_ascii=False, indent=2))
    elif args.command == "list":
        print("\n".join(store.list_ids()) or "No profiles found.")
    elif args.command == "export":
        print(store.export_profile(args.id, args.destination))
    elif args.command == "import":
        print(store.import_profile(args.source))
    elif args.command == "audit":
        result = audit_brief(json.loads(args.source.read_text(encoding="utf-8")), tuple(args.required))
        print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))
        if not result.complete:
            raise SystemExit(2)
    elif args.command == "prompt":
        print(drafting_prompt(store.load(args.id), args.brief.read_text(encoding="utf-8")))

if __name__ == "__main__":
    main()
