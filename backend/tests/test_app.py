from __future__ import annotations

import uuid

import pytest

from app.client import App
from app.client.entity import Account
from app.domain.volunteers.exceptions import (
    TokenInvalidError,
    AccountNotFoundError,
)


@pytest.mark.asyncio
class TestApp:
    async def test_get_client_account(
        self,
        app: App,
        account: Account,
    ) -> None:
        app.use_account(account.id)
        client_account = await app.accounts.get_client()
        assert client_account.id == account.id


    async def test_get_client_account_invalid_token(
        self,
        app: App,
    ) -> None:
        app.use_account(None)
        with pytest.raises(TokenInvalidError):
            await app.accounts.get_client()

        app.use_account(uuid.uuid4())
        with pytest.raises(AccountNotFoundError):
            await app.accounts.get_client()
