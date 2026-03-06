from __future__ import annotations

import uuid

import pytest

from app.client import App
from app.client.entity import Account, Applicant
from app.domain.applicants.schema import ApplicantCreate, ApplicantUpdate
from app.domain.applicants.enums import ApplicantStatus, ProfessionalInterest
from app.domain.volunteers.exceptions import TokenInvalidError
from app.exceptions import ForbiddenError, NotFoundError


@pytest.mark.asyncio
class TestCreateApplicant:
    """POST /applicants/ — public endpoint, no auth required."""

    async def test_create_minimal(self, app: App) -> None:
        app.use_account(None)
        applicant = await app.applicants.create(ApplicantCreate(
            first_name="Anna",
            last_name="Kovács",
            email=f"{uuid.uuid4()}@example.com",
            privacy_accepted=True,
        ))
        assert applicant.data.first_name == "Anna"
        assert applicant.data.last_name == "Kovács"
        assert applicant.data.interests == []
        assert applicant.data.privacy_accepted is True
        assert applicant.data.status == ApplicantStatus.received

    async def test_create_with_interests(self, app: App) -> None:
        app.use_account(None)
        interests = [
            ProfessionalInterest.communication,
            ProfessionalInterest.it_digital,
        ]
        applicant = await app.applicants.create(ApplicantCreate(
            first_name="Béla",
            last_name="Nagy",
            email=f"{uuid.uuid4()}@example.com",
            interests=interests,
            privacy_accepted=True,
        ))
        assert applicant.data.interests == [str(i) for i in interests]

    async def test_create_all_interests(self, app: App) -> None:
        app.use_account(None)
        all_interests = list(ProfessionalInterest)
        applicant = await app.applicants.create(ApplicantCreate(
            first_name="Csaba",
            last_name="Szabó",
            email=f"{uuid.uuid4()}@example.com",
            interests=all_interests,
            privacy_accepted=True,
        ))
        assert len(applicant.data.interests) == len(all_interests)

    async def test_create_without_privacy_accepted(self, app: App) -> None:
        app.use_account(None)
        applicant = await app.applicants.create(ApplicantCreate(
            first_name="Dóra",
            last_name="Tóth",
            email=f"{uuid.uuid4()}@example.com",
            privacy_accepted=False,
        ))
        assert applicant.data.privacy_accepted is False

    async def test_create_default_status_is_received(self, app: App) -> None:
        app.use_account(None)
        applicant = await app.applicants.create(ApplicantCreate(
            first_name="Erika",
            last_name="Kiss",
            email=f"{uuid.uuid4()}@example.com",
            privacy_accepted=True,
        ))
        assert applicant.data.status == ApplicantStatus.received

    async def test_create_duplicate_email_allowed(self, app: App) -> None:
        """Email is not unique — multiple applications from the same address are allowed."""
        app.use_account(None)
        email = f"{uuid.uuid4()}@example.com"
        a1 = await app.applicants.create(ApplicantCreate(
            first_name="Ferenc",
            last_name="Varga",
            email=email,
            privacy_accepted=True,
        ))
        a2 = await app.applicants.create(ApplicantCreate(
            first_name="Ferenc",
            last_name="Varga",
            email=email,
            privacy_accepted=True,
        ))
        assert a1.id != a2.id


@pytest.mark.asyncio
class TestListApplicants:
    """GET /applicants/ — requires moderator or admin role."""

    async def test_list_as_admin(
        self,
        app: App,
        admin_account: Account,
        applicant: Applicant,
    ) -> None:
        app.use_account(admin_account.id)
        result = await app.applicants.list()
        assert result.total >= 1

    async def test_list_as_moderator(
        self,
        app: App,
        moderator_account: Account,
        applicant: Applicant,
    ) -> None:
        app.use_account(moderator_account.id)
        result = await app.applicants.list()
        assert result.total >= 1

    async def test_list_as_member_forbidden(
        self,
        app: App,
        member_account: Account,
    ) -> None:
        app.use_account(member_account.id)
        with pytest.raises(ForbiddenError):
            await app.applicants.list()

    async def test_list_unauthenticated_forbidden(
        self,
        app: App,
    ) -> None:
        app.use_account(None)
        with pytest.raises(TokenInvalidError):
            await app.applicants.list()

    async def test_list_pagination(
        self,
        app: App,
        admin_account: Account,
    ) -> None:
        app.use_account(None)
        for i in range(3):
            await app.applicants.create(ApplicantCreate(
                first_name=f"Page{i}",
                last_name="Test",
                email=f"{uuid.uuid4()}@example.com",
                privacy_accepted=True,
            ))

        app.use_account(admin_account.id)
        result = await app.applicants.list(currentPage=1, pageSize=2)
        assert len(result.items) <= 2


@pytest.mark.asyncio
class TestGetApplicant:
    """GET /applicants/{id} — requires moderator or admin role."""

    async def test_get_as_admin(
        self,
        app: App,
        admin_account: Account,
        applicant: Applicant,
    ) -> None:
        app.use_account(admin_account.id)
        fetched = await app.applicants.get(applicant.id)
        assert fetched.id == applicant.id
        assert fetched.data.first_name == applicant.data.first_name

    async def test_get_as_moderator(
        self,
        app: App,
        moderator_account: Account,
        applicant: Applicant,
    ) -> None:
        app.use_account(moderator_account.id)
        fetched = await app.applicants.get(applicant.id)
        assert fetched.id == applicant.id

    async def test_get_as_member_forbidden(
        self,
        app: App,
        member_account: Account,
        applicant: Applicant,
    ) -> None:
        app.use_account(member_account.id)
        with pytest.raises(ForbiddenError):
            await app.applicants.get(applicant.id)

    async def test_get_nonexistent(
        self,
        app: App,
        admin_account: Account,
    ) -> None:
        app.use_account(admin_account.id)
        with pytest.raises(NotFoundError):
            await app.applicants.get(uuid.uuid4())


@pytest.mark.asyncio
class TestUpdateApplicant:
    """PUT /applicants/{id} — status update, requires moderator or admin."""

    async def test_update_status_to_accepted(
        self,
        app: App,
        admin_account: Account,
        applicant: Applicant,
    ) -> None:
        assert applicant.data.status == ApplicantStatus.received

        app.use_account(admin_account.id)
        updated = await app.applicants.update(
            applicant.id,
            ApplicantUpdate(status=ApplicantStatus.accepted),
        )
        assert updated.data.status == ApplicantStatus.accepted

    async def test_update_as_moderator(
        self,
        app: App,
        moderator_account: Account,
        applicant: Applicant,
    ) -> None:
        app.use_account(moderator_account.id)
        updated = await app.applicants.update(
            applicant.id,
            ApplicantUpdate(status=ApplicantStatus.accepted),
        )
        assert updated.data.status == ApplicantStatus.accepted

    async def test_update_as_member_forbidden(
        self,
        app: App,
        member_account: Account,
        applicant: Applicant,
    ) -> None:
        app.use_account(member_account.id)
        with pytest.raises(ForbiddenError):
            await app.applicants.update(
                applicant.id,
                ApplicantUpdate(status=ApplicantStatus.accepted),
            )

    async def test_update_unauthenticated_forbidden(
        self,
        app: App,
        applicant: Applicant,
    ) -> None:
        app.use_account(None)
        with pytest.raises(TokenInvalidError):
            await app.applicants.update(
                applicant.id,
                ApplicantUpdate(status=ApplicantStatus.accepted),
            )

    async def test_update_preserves_other_fields(
        self,
        app: App,
        admin_account: Account,
        applicant: Applicant,
    ) -> None:
        original_name = applicant.data.first_name
        original_email = applicant.data.email

        app.use_account(admin_account.id)
        updated = await app.applicants.update(
            applicant.id,
            ApplicantUpdate(status=ApplicantStatus.accepted),
        )
        assert updated.data.first_name == original_name
        assert updated.data.email == original_email

    async def test_update_nonexistent_applicant(
        self,
        app: App,
        admin_account: Account,
    ) -> None:
        app.use_account(admin_account.id)
        with pytest.raises(NotFoundError):
            await app.applicants.update(
                uuid.uuid4(),
                ApplicantUpdate(status=ApplicantStatus.accepted),
            )
