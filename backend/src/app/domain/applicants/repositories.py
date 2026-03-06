from __future__ import annotations

from app.contrib.litestar import SQLAlchemyAsyncRepository
from app.models.applicant import Applicant


__all__ = [
    "ApplicantRepository",
]


class ApplicantRepository(SQLAlchemyAsyncRepository[Applicant]):
    model_type = Applicant
