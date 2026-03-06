from __future__ import annotations

import typing as t
from types import NoneType
from uuid import UUID

import msgspec
import httpx

from app.exceptions import ErrorMeta
from app.contrib.litestar import OffsetPagination
from app.contrib.litestar.factory import enc_hook, dec_hook
from app.domain.volunteers.auth import create_claims, issue_token


T = t.TypeVar("T")


class Client:
    """
    Feature-less HTTP client.
    """
    def __init__(
        self, 
        client: httpx.AsyncClient,
        path: str = "",
    ):
        self._client = client
        self._path = path


    def dec_hook(
        self,
        typ: type[t.Any],
        obj: t.Any,
    ) -> t.Any:
        raise TypeError(f"Unsupported type for decoding: {typ}")


    @classmethod
    async def from_url(
        cls, 
        base_url: str,
        auth: tuple[str, str] | None = None,
    ):
        client = httpx.AsyncClient(
            base_url=base_url, 
            auth=auth,
        )
        return cls(client)


    @staticmethod
    def raise_for_status(response: httpx.Response) -> None:
        if response.status_code >= 300:
            body = response.json()
            raise ErrorMeta.reconstruct(body)


    def get_client(self) -> httpx.AsyncClient:
        return self._client
    

    def get_path(self) -> str:
        return self._path


    def set_cookie(self, name: str, value: str) -> None:
        self._client.cookies.set(name, value)


    @t.overload
    async def request(
        self,
        method: str,
        url: str,
        type: type[T],
        *,
        body: t.Any = None,
        **params: t.Any,
    ) -> T:
        ...


    @t.overload
    async def request(
        self,
        method: str,
        url: str,
        *,
        body: t.Any = None,
        **params: t.Any,
    ) -> None:
        ...


    async def request(
        self,
        method: str,
        url: str,
        type: type[T] | None = None,
        *,
        body: t.Any = None,
        **params: t.Any,
    ) -> T | None:
        response = await self._client.request(
            method=method, 
            url=self._path + url, 
            params=params, 
            json=msgspec.to_builtins(body, enc_hook=enc_hook),
        )

        self.raise_for_status(response)

        if type is None:
            return
        
        body = response.read()

        return msgspec.json.decode(body, type=type, dec_hook=self.dec_hook)


    async def get(
        self, 
        url: str, 
        type: type[T],
        **params: t.Any,
    ) -> T:
        return await self.request("GET", url, type, **params)
    

    async def post(
        self,
        url: str,
        type: type[T] | None = None, 
        *,
        body: t.Any = None,
        **params: t.Any,
    ) -> T:
        if type is None:
            return await self.request("POST", url, body=body, **params)
        else:
            return await self.request("POST", url, type, body=body, **params)
    
    
    async def put(
        self,
        url: str,
        type: type[T] | None = None,
        *,
        body: t.Any = None,
        **params: t.Any,
    ) -> T:
        if type is None:
            return await self.request("PUT", url, body=body, **params)
        else:
            return await self.request("PUT", url, type, body=body, **params)
    

    async def patch(
        self,
        url: str,
        type: type[T] | None = None,
        *,
        body: t.Any = None,
        **params: t.Any,
    ) -> T:
        if type is None:
            return await self.request("PATCH", url, body=body, **params)
        else:
            return await self.request("PATCH", url, type, body=body, **params)
    

    async def delete(
        self,
        url: str,
        type: type[T] | None = None,
        **params: t.Any,
    ) -> T:
        if type is None:
            return await self.request("DELETE", url, **params)
        else:
            return await self.request("DELETE", url, type, **params)


SchemaT = t.TypeVar("SchemaT")
CreateT = t.TypeVar("CreateT")
UpdateT = t.TypeVar("UpdateT")
EntityT = t.TypeVar("EntityT", bound="Entity")


def get_entity_type(attr_type):
    origin = t.get_origin(attr_type)

    if origin is None:
        if issubclass(attr_type, Entity):
            return attr_type
        else:
            return None

    real_type, none_type = t.get_args(attr_type)
    
    if real_type is not type(None) and issubclass(real_type, Entity):
        return real_type
    
    return None


class Object(t.Generic[SchemaT]):
    schema_type: t.Type[SchemaT]


    def __init__(self, data: SchemaT, app: AppBase):
        self.data = data
        self.app = app

        type_hints = t.get_type_hints(self.__class__)
        for attr_name, attr_type in type_hints.items():
            try:
                entity_type = get_entity_type(attr_type)
            except:
                continue

            if entity_type is None:
                continue

            related_data = getattr(self.data, attr_name, None)
            if related_data is None:
                setattr(self, attr_name, None)
                continue

            related_entity = entity_type(
                data=related_data,
                app=app,
            )

            setattr(self, attr_name, related_entity)


class Entity(Object[SchemaT], t.Generic[SchemaT]):
    data: SchemaT


    @property
    def id(self) -> UUID:
        return getattr(self.data, "id")


    @property
    def path(self) -> str:
        return f"{self.collection.path}/{self.id}"


    def __init__(self, data: SchemaT, app: AppBase):
        super().__init__(data=data, app=app)
        self.collection = app.get_collection(self.__class__)
    

    async def refresh(self) -> None:
        obj = await self.collection.get(self.id)
        self.data = obj.data
    

    def _construct_update_obj(self):
        update_type = self.collection.update_type
        type_hints = t.get_type_hints(update_type)
        update_fields = {}

        for field_name in type_hints.keys():
            if hasattr(self.data, field_name):
                update_fields[field_name] = getattr(self.data, field_name)
            
            stripped = field_name.removesuffix("_id")
            if hasattr(self, stripped):
                related_entity = getattr(self, stripped)
                if related_entity is not None:
                    update_fields[field_name] = related_entity.id
        
        return update_type(**update_fields)
    

    async def save(self) -> None:
        update_obj = self._construct_update_obj()
        obj = await self.collection.update(self.id, update_obj)
        self.data = obj.data
    

    async def delete(self) -> None:
        await self.collection.delete(self.id)


class Collection(t.Generic[EntityT, CreateT, UpdateT]):
    path: t.ClassVar[str]
    entity_type: t.Type[EntityT]
    create_type: t.Type[CreateT]
    update_type: t.Type[UpdateT]


    def __init__(self, app: AppBase, *args, **kwargs):
        self.app = app
    

    async def list(
        self,
        **params: t.Any,
    ) -> OffsetPagination[EntityT]:
        return await self.app.get(
            url=self.path, 
            type=OffsetPagination[self.entity_type],
            **params,
        )
    

    async def get(
        self,
        item_id: UUID,
    ) -> EntityT:
        return await self.app.get(
            url=f"{self.path}/{item_id}",
            type=self.entity_type,
        )
    

    async def create(
        self,
        data: CreateT,
    ) -> EntityT:
        return await self.app.post(
            url=self.path,
            type=self.entity_type,
            body=data,
        )
    
    
    async def update(
        self,
        item_id: UUID,
        data: UpdateT,
    ) -> EntityT:
        return await self.app.put(
            url=f"{self.path}/{item_id}",
            type=self.entity_type,
            body=data,
        )
    

    async def delete(
        self,
        item_id: UUID,
    ) -> None:
        await self.app.delete(
            url=f"{self.path}/{item_id}",
        )


class AppBase(Client):
    def __init__(self, client: httpx.AsyncClient, *args, **kwargs):
        super().__init__(client=client, *args, **kwargs)
        
        self._collections: dict[t.Type, Collection] = {}

        type_hints = t.get_type_hints(self.__class__)
        for attr_name, attr_type in type_hints.items():
            if issubclass(attr_type, Collection):
                collection_instance = attr_type(app=self)
                self._collections[attr_type.entity_type] = collection_instance  # type: ignore
                setattr(self, attr_name, collection_instance)
    

    def dec_hook(
        self,
        type: t.Type,
        obj: t.Any,
    ) -> t.Any:
        try:
            return dec_hook(type, obj)
        except:
            pass

        data = msgspec.convert(
            obj, 
            type=type.schema_type,
            dec_hook=self.dec_hook,
        )
        return type(data=data, app=self)


    def get_collection(
        self,
        entity_type: t.Type[EntityT],
    ) -> Collection[EntityT, t.Any, t.Any]:
        return self._collections[entity_type]
    

    def auth(self, token: str) -> None:
        self.set_cookie("Auth", token)
        self.set_cookie("__Secure-Auth", token)
    

    def use_account(
        self,
        account_id: UUID | str | None,
    ) -> None:
        if account_id is None:
            self.auth("")
            return

        if isinstance(account_id, str):
            account_id = UUID(account_id)

        claims = create_claims(account_id=account_id)
        token = issue_token(claims)
        self.auth(token)
