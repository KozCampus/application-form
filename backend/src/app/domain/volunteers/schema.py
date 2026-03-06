from __future__ import annotations

from app.contrib.msgspec import UUIDAudit, Struct
from app.domain.volunteers.enums import AccountRole


class AccountSchema(UUIDAudit):
    name: str
    email: str
    is_active: bool
    role: AccountRole


class AccountCreate(Struct):
    name: str
    email: str
    is_active: bool = False
    role: AccountRole = AccountRole.member


class AccountUpdate(Struct):
    name: str
    email: str
    is_active: bool
    role: AccountRole
