from __future__ import annotations

import typing as t
from uuid import UUID

from app.contrib.litestar import *  # type: ignore
from app.domain.applicants.schema import (
    ApplicantSchema,
    ApplicantCreate,
    ApplicantUpdate,
)
from app.domain.applicants.services import ApplicantService
from app.models import Account


class ApplicantController(Controller):
    path = "/applicants"
    tags = ["Applicants"]


    @post(
        operation_id="CreateApplicant",
        path="/",
    )
    async def create_applicant(
        self,
        data: ApplicantCreate,
        applicant_service: ApplicantService,
    ) -> ApplicantSchema:
        applicant = await applicant_service.create(data)
        return applicant_service.to_schema(
            data=applicant,
            schema_type=ApplicantSchema,
        )


    @get(
        operation_id="ListApplicants",
        path="/",
    )
    async def list_applicants(
        self,
        applicant_service: ApplicantService,
        filters: t.Annotated[
            list[FilterTypes],
            Dependency(skip_validation=True),
        ],
        moderator_account: Account,
    ) -> OffsetPagination[ApplicantSchema]:
        results, total = await applicant_service.list_and_count(*filters)
        return applicant_service.to_schema(
            data=results,
            total=total,
            schema_type=ApplicantSchema,
            filters=filters,
        )


    @get(
        operation_id="GetApplicant",
        path="/{applicant_id:uuid}",
    )
    async def get_applicant(
        self,
        applicant_id: UUID,
        applicant_service: ApplicantService,
        moderator_account: Account,
    ) -> ApplicantSchema:
        applicant = await applicant_service.get(applicant_id)
        return applicant_service.to_schema(
            data=applicant,
            schema_type=ApplicantSchema,
        )


    @put(
        operation_id="UpdateApplicant",
        path="/{applicant_id:uuid}",
    )
    async def update_applicant(
        self,
        applicant_id: UUID,
        data: ApplicantUpdate,
        applicant_service: ApplicantService,
        moderator_account: Account,
    ) -> ApplicantSchema:
        applicant = await applicant_service.get(applicant_id)
        applicant.status = data.status
        return applicant_service.to_schema(
            data=applicant,
            schema_type=ApplicantSchema,
        )
