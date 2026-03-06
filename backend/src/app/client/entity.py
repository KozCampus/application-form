from __future__ import annotations

from app.client.primitives import Entity
from app.domain.applicants.schema import ApplicantSchema
from app.domain.volunteers.schema import (
    AccountSchema,
)


class Account(Entity[AccountSchema]):
    schema_type = AccountSchema


class Applicant(Entity[ApplicantSchema]):
    schema_type = ApplicantSchema
