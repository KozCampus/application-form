from __future__ import annotations

from app.client.primitives import Client, Entity, Collection, AppBase
from app.client.collection import AccountCollection, ApplicantCollection


__all__ = [
    "Client",
    "Entity",
    "Collection",
    "AppBase",
    "App",
]


class App(AppBase):
    accounts: AccountCollection
    applicants: ApplicantCollection
