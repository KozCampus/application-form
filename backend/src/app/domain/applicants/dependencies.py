from __future__ import annotations

from app.contrib.litestar import Provide, create_service_provider
from app.domain.applicants.services import ApplicantService


__all__ = [
    "get_applicants_dependencies",
]


provide_applicant_service = create_service_provider(ApplicantService)


def get_applicants_dependencies():
    return {
        "applicant_service": Provide(provide_applicant_service),
    }
