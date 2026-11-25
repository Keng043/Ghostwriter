"""Local profile storage with atomic writes and no cloud sync."""
import json
import os
import re
import tempfile
from pathlib import Path
from .models import StyleProfile

def default_data_dir() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
        return base / "Ghostwriter" / "profiles"
    base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
    return base / "ghostwriter" / "profiles"

def safe_id(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip()).strip("-").lower()
    if not slug:
        raise ValueError("Profile ID must contain letters or numbers")
    return slug[:64]

class ProfileStore:
    def __init__(self, directory: Path | None = None):
        self.directory = Path(directory) if directory else default_data_dir()
        self.directory.mkdir(parents=True, exist_ok=True)

    def path_for(self, user_id: str) -> Path:
        return self.directory / f"{safe_id(user_id)}.json"

    def save(self, profile: StyleProfile) -> Path:
        profile.validate()
        target = self.path_for(profile.user_id)
        payload = json.dumps(profile.to_dict(), ensure_ascii=False, indent=2)
        fd, temporary = tempfile.mkstemp(dir=self.directory, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(payload + "\n")
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        return target

    def load(self, user_id: str) -> StyleProfile:
        path = self.path_for(user_id)
        if not path.exists():
            raise FileNotFoundError(f"No profile found for '{user_id}'")
        return StyleProfile.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def list_ids(self) -> list[str]:
        return sorted(path.stem for path in self.directory.glob("*.json"))

    def export_profile(self, user_id: str, destination: Path) -> Path:
        profile = self.load(user_id)
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(profile.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return destination

    def import_profile(self, source: Path) -> Path:
        profile = StyleProfile.from_dict(json.loads(Path(source).read_text(encoding="utf-8")))
        return self.save(profile)
