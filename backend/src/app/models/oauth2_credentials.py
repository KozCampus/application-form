from __future__ import annotations

from app.contrib.sqlalchemy import *  # type: ignore


class OAuth2Credentials(UUIDAuditBase):
    __tablename__ = "oauth2_credentials"

    access_token: Mapped[str] = mapped_column()
