from __future__ import annotations

import typing as t
from uuid import UUID

from app.contrib.litestar import *  # type: ignore
from app.contrib.sqlalchemy import update
from app.domain.volunteers.auth import (
    create_claims,
    issue_token,
    check_registration_token,
    get_auth_cookie,
    set_auth_cookie,
)
from app.exceptions import (
    ForbiddenError,
    BadRequestError,
)
from app.domain.volunteers.schema import (
    AccountSchema,
    AccountCreate,
    AccountUpdate,
)
from app.domain.volunteers.services import AccountService
from app.models import Account
from app.domain.volunteers.enums import AccountRole


class AccountController(Controller):
    path = "/accounts"
    tags = ["Accounts"]


    @get(
        operation_id="GetClientAccount",
        path="/me",
    )
    async def get_client_account(
        self,
        prospect_account: Account,
        account_service: AccountService,
    ) -> AccountSchema:
        return account_service.to_schema(
            data=prospect_account,
            schema_type=AccountSchema,
        )


    @post(
        operation_id="CreateClientAccount",
        path="/me",
    )
    async def create_client_account(
        self,
        request: Request,
        data: AccountCreate,
        account_service: AccountService,
    ) -> Response[AccountSchema]:
        if data.is_active or data.role != AccountRole.member:
            raise BadRequestError()

        reg_token = get_auth_cookie(request, key="Reg")

        if reg_token is None:
            raise ForbiddenError()

        email, credentials_id = check_registration_token(reg_token)

        if email is None or email != data.email:
            raise ForbiddenError()

        account = await account_service.create(data)
        account.google_credentials_id = credentials_id

        claims = create_claims(account.id)
        token = issue_token(claims)

        obj = account_service.to_schema(
            data=account,
            schema_type=AccountSchema,
        )
        response = Response[AccountSchema](obj)
        set_auth_cookie(response, token)
        return response


    @get(
        operation_id="ListAccounts",
        path="/",
    )
    async def list_accounts(
        self,
        account_service: AccountService,
        filters: t.Annotated[
            list[FilterTypes],
            Dependency(skip_validation=True),
        ],
        admin_account: Account,
    ) -> OffsetPagination[AccountSchema]:
        results, total = await account_service.list_and_count(*filters)
        return account_service.to_schema(
            data=results,
            total=total,
            schema_type=AccountSchema,
            filters=filters,
        )


    @post(
        operation_id="CreateAccount",
        path="/",
    )
    async def create_account(
        self,
        data: AccountCreate,
        account_service: AccountService,
        admin_account: Account,
    ) -> AccountSchema:
        account = await account_service.create(data)
        return account_service.to_schema(
            data=account,
            schema_type=AccountSchema,
        )


    @get(
        operation_id="GetAccount",
        path="/{account_id:uuid}",
    )
    async def get_account(
        self,
        account_id: UUID,
        account_service: AccountService,
        admin_account: Account,
    ) -> AccountSchema:
        account = await account_service.get(account_id)
        return account_service.to_schema(
            data=account,
            schema_type=AccountSchema,
        )


    @put(
        operation_id="UpdateAccount",
        path="/{account_id:uuid}",
    )
    async def update_account(
        self,
        account_id: UUID,
        data: AccountUpdate,
        account_service: AccountService,
        admin_account: Account,
    ) -> AccountSchema:
        account = await account_service.get(account_id)
        update(account, data)

        return account_service.to_schema(
            data=account,
            schema_type=AccountSchema,
        )


    @delete(
        operation_id="DeleteAccount",
        path="/{account_id:uuid}",
    )
    async def delete_account(
        self,
        account_id: UUID,
        account_service: AccountService,
        admin_account: Account,
    ) -> None:
        await account_service.delete(item_id=account_id)
