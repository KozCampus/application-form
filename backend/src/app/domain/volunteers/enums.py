from __future__ import annotations

from enum import StrEnum


class AccountRole(StrEnum):
    member = "member"
    moderator = "moderator"
    admin = "admin"
