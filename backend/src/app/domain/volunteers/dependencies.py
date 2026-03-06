from __future__ import annotations

from litestar import Request

from app.contrib.litestar import Provide, create_service_provider
from app.domain.volunteers.services import (
    AccountService,
    OAuth2CredentialsService,
)
from app.models import Account
from app.domain.volunteers.enums import AccountRole
from app.domain.volunteers.auth import Claims, get_claims_from_cookies
from app.exceptions import ForbiddenError
from app.domain.volunteers.exceptions import (
    AccountNotFoundError,
    InactiveAccountError,
)


__all__ = [
    "get_volunteers_dependencies",
    "provide_account_service",
    "provide_oauth2_credentials_service",
    "provide_claims",
    "provide_prospect_account",
    "provide_account",
    "provide_admin_account",
    "provide_moderator_account",
]


def get_volunteers_dependencies():
    return {
        "account_service": Provide(provide_account_service),
        "oauth2_credentials_service": Provide(provide_oauth2_credentials_service),
        "claims": Provide(provide_claims),
        "prospect_account": Provide(provide_prospect_account),
        "account": Provide(provide_account),
        "admin_account": Provide(provide_admin_account),
        "moderator_account": Provide(provide_moderator_account),
    }


provide_account_service = create_service_provider(AccountService)
provide_oauth2_credentials_service = create_service_provider(OAuth2CredentialsService)


async def provide_claims(
    request: Request,
) -> Claims | None:
    return get_claims_from_cookies(request.cookies)


async def provide_prospect_account(
    account_service: AccountService,
    claims: Claims,
) -> Account:
    account = await account_service.get_one_or_none(id=claims.sub)

    if account is None:
        raise AccountNotFoundError()

    return account


async def provide_account(
    prospect_account: Account,
) -> Account:
    if not prospect_account.is_active:
        raise InactiveAccountError()

    return prospect_account


async def provide_admin_account(account: Account) -> Account:
    if account.role != AccountRole.admin:
        raise ForbiddenError()

    return account


async def provide_moderator_account(account: Account) -> Account:
    if account.role not in (AccountRole.moderator, AccountRole.admin):
        raise ForbiddenError()

    return account
