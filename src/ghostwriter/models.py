"""Validated data structures for user-owned writing profiles."""
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

STYLE_FIELDS = (
    "tone", "sentence_architecture", "lexical_choice", "punctuation_spacing",
    "formatting", "opening", "bad_news_framing", "negative_constraints",
)

@dataclass
class StyleProfile:
    user_id: str
    display_name: str = "Writer"
    language: str = "en"
    style_dna: dict[str, Any] = field(default_factory=dict)
    preferences: dict[str, Any] = field(default_factory=dict)
    retain_samples: bool = False
    samples: list[str] = field(default_factory=list)
    version: str = "1.0"
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def validate(self) -> None:
        if not self.user_id or not self.user_id.strip():
            raise ValueError("user_id must not be empty")
        unknown = set(self.style_dna) - set(STYLE_FIELDS)
        if unknown:
            raise ValueError(f"Unknown style fields: {', '.join(sorted(unknown))}")
        if not self.retain_samples and self.samples:
            raise ValueError("Samples cannot be stored unless retain_samples is true")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StyleProfile":
        allowed = set(cls.__dataclass_fields__)
        profile = cls(**{key: value for key, value in data.items() if key in allowed})
        profile.validate()
        return profile
