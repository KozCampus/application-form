from __future__ import annotations

from app.client.primitives import Collection
from app.client.entity import Account
from app.domain.volunteers.schema import (
    AccountCreate,
    AccountUpdate,
)


class AccountCollection(Collection[Account, AccountCreate, AccountUpdate]):
    path = "/accounts"
    entity_type = Account
    create_type = AccountCreate
    update_type = AccountUpdate


    async def get_client(self) -> Account:
        return await self.app.get(
            url=f"{self.path}/me",
            type=self.entity_type,
        )


    async def create_client(self, data: AccountCreate) -> Account:
        return await self.app.post(
            url=f"{self.path}/me",
            type=self.entity_type,
            data=data,
        )
