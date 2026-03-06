from __future__ import annotations

from app.contrib.litestar import SQLAlchemyAsyncRepository
from app.models import (
    Account,
    OAuth2Credentials,
)


__all__ = [
    "AccountRepository",
    "OAuth2CredentialsRepository",
]


class AccountRepository(SQLAlchemyAsyncRepository[Account]):
    model_type = Account


class OAuth2CredentialsRepository(SQLAlchemyAsyncRepository[OAuth2Credentials]):
    model_type = OAuth2Credentials
