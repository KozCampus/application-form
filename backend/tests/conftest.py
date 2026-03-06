from __future__ import annotations

from collections.abc import AsyncIterator
from uuid import uuid4

import pytest_asyncio
from litestar.testing import AsyncTestClient

from app.server.asgi import app as asgi_app
from app.client import App
from app.client.entity import Account
from app.domain.volunteers.services import AccountService
from app.domain.volunteers.schema import AccountCreate
from app.domain.volunteers.enums import AccountRole


asgi_app.debug = True


@pytest_asyncio.fixture(scope="session")
async def app() -> AsyncIterator[App]:
    async with AsyncTestClient(app=asgi_app) as client:
        yield App(client)


@pytest_asyncio.fixture(scope="session")
async def admin_account(app: App):
    init_account_id = "00000000-0000-0000-0000-000000000001"

    app.use_account(init_account_id)

    account = await app.accounts.create(AccountCreate(
        name="Test Admin",
        email=f"{uuid4()}@example.com",
        is_active=True,
        role=AccountRole.admin,
    ))

    yield account

    app.use_account(init_account_id)
    await account.delete()


@pytest_asyncio.fixture(scope="function", params=list(AccountRole))
async def account(
    app: App,
    admin_account: Account,
    request,
):
    role = request.param

    app.use_account(admin_account.id)

    account = await app.accounts.create(AccountCreate(
        name=f"Test {role.value.capitalize()}",
        email=f"{uuid4()}@example.com",
        is_active=True,
        role=role,
    ))

    yield account

    app.use_account(admin_account.id)
    await account.delete()
