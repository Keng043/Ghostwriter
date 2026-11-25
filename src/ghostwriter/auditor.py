"""Strict completeness checks. This module never invents missing facts."""
from dataclasses import dataclass, field
from typing import Any

@dataclass
class AuditResult:
    complete: bool
    missing: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)

def audit_brief(data: dict[str, Any], required: tuple[str, ...] = ()) -> AuditResult:
    missing = [key for key in required if key not in data or data[key] in (None, "", [], {})]
    conflicts = []
    for key, value in data.items():
        if isinstance(value, dict) and value.get("conflict") is True:
            conflicts.append(str(value.get("description") or key))
    return AuditResult(not missing and not conflicts, missing, conflicts)

def build_clarification_questions(result: AuditResult) -> list[str]:
    questions = [f"What is the {field.replace('_', ' ')}?" for field in result.missing]
    questions.extend(f"Please resolve this conflicting information: {item}" for item in result.conflicts)
    return questions[:5]
