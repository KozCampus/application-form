from __future__ import annotations

from app.contrib.litestar import SQLAlchemyAsyncRepositoryService
from app.models.applicant import Applicant
from app.domain.applicants.repositories import ApplicantRepository


__all__ = [
    "ApplicantService",
]


class ApplicantService(SQLAlchemyAsyncRepositoryService[Applicant]):
    repository_type = ApplicantRepository
