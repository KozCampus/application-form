from __future__ import annotations

from app.contrib.sqlalchemy import *  # type: ignore
from app.domain.applicants.enums import ApplicantStatus


class Applicant(UUIDAuditBase):
    __tablename__ = "applicant"

    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    interests: Mapped[list] = mapped_column(JSONB)
    status: Mapped[ApplicantStatus] = mapped_column(default=ApplicantStatus.received)
