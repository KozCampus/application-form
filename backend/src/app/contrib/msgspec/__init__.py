from __future__ import annotations

import typing as t
from datetime import date, datetime, time, timezone
from uuid import UUID
from enum import Enum, StrEnum

import msgspec
from msgspec import Struct as _Struct
from msgspec import field


__all__ = [
    "t",
    "UUID",
    "date",
    "datetime",
    "time",
    "timezone",
    "Enum",
    "StrEnum",
    "msgspec",
    "Struct",
    "field",
    "UUIDAudit",
]


class Struct(_Struct, rename="camel"):
    def to_dict(self) -> dict[str, t.Any]:
        return msgspec.to_builtins(
            obj=self, 
            builtin_types={date, datetime, time, UUID},
        )


class UUIDAudit(Struct):
    id: UUID
    created_at: datetime
    updated_at: datetime
