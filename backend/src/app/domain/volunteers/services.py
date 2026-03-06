from __future__ import annotations

from app.contrib.litestar import SQLAlchemyAsyncRepositoryService
from app.models import (
    Account,
    OAuth2Credentials,
)
from app.domain.volunteers.repositories import (
    AccountRepository,
    OAuth2CredentialsRepository,
)


__all__ = [
    "AccountService",
    "OAuth2CredentialsService",
]


class AccountService(SQLAlchemyAsyncRepositoryService[Account]):
    repository_type = AccountRepository


class OAuth2CredentialsService(SQLAlchemyAsyncRepositoryService[OAuth2Credentials]):
    repository_type = OAuth2CredentialsRepository
