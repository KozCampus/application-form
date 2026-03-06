from __future__ import annotations

from app.domain.volunteers.controllers import (
    AccountController,
    AuthController,
)


__all__ = [
    "get_volunteers_routes",
]


def get_volunteers_routes():
    return [
        AccountController,
        AuthController,
    ]
