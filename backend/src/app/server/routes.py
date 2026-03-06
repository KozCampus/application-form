from __future__ import annotations

from app.domain.volunteers.routes import get_volunteers_routes


__all__ = [
    "get_routes",
]


def get_routes():
    return get_volunteers_routes()
