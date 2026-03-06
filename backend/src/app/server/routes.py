from __future__ import annotations

from app.domain.applicants.routes import get_applicants_routes
from app.domain.volunteers.routes import get_volunteers_routes


__all__ = [
    "get_routes",
]


def get_routes():
    return [
        *get_volunteers_routes(),
        *get_applicants_routes(),
    ]
