from __future__ import annotations

from app.domain.applicants.dependencies import get_applicants_dependencies
from app.domain.volunteers.dependencies import get_volunteers_dependencies


__all__ = [
    "get_dependencies",
]


def get_dependencies():
    return {
        **get_volunteers_dependencies(),
        **get_applicants_dependencies(),
    }
