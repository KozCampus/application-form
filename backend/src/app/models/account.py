from __future__ import annotations

import typing as t

from app.contrib.sqlalchemy import *  # type: ignore
from app.domain.volunteers.enums import AccountRole

if t.TYPE_CHECKING:
    from app.models.oauth2_credentials import OAuth2Credentials


class Account(UUIDAuditBase):
    __tablename__ = "account"

    name: Mapped[str | None] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=False)
    role: Mapped[AccountRole] = mapped_column(default=AccountRole.member)

    google_credentials_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("oauth2_credentials.id"),
    )

    google_credentials: Mapped[OAuth2Credentials | None] = relationship(
        lazy="joined",
    )
