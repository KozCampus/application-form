from __future__ import annotations

from app.domain.applicants.controllers import ApplicantController


__all__ = [
    "get_applicants_routes",
]


def get_applicants_routes():
    return [
        ApplicantController,
    ]
