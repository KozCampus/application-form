from __future__ import annotations

from app.contrib.msgspec import UUIDAudit, Struct, field
from app.domain.applicants.enums import (
    ApplicantStatus, 
    ProfessionalInterest,
)


class ApplicantSchema(UUIDAudit):
    first_name: str
    last_name: str
    email: str
    interests: list[ProfessionalInterest]
    privacy_accepted: bool
    status: ApplicantStatus


class ApplicantCreate(Struct):
    first_name: str
    last_name: str
    email: str
    interests: list[ProfessionalInterest] = field(default_factory=list)
    privacy_accepted: bool = False


class ApplicantUpdate(Struct):
    status: ApplicantStatus
