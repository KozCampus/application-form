from __future__ import annotations

import typing as t
from contextlib import AbstractAsyncContextManager, asynccontextmanager

import msgspec
from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar_saq import QueueConfig
from app.contrib.litestar.dependencies import *  # type: ignore
from app.contrib.litestar.domain.system import HealthController
from app.contrib.litestar.exception_handler import exception_handler
from app.contrib.litestar.openapi import create_openapi_config
from app.contrib.litestar.plugins import (
    create_cors_config,
    create_saq_plugin,
)
from app.contrib.sqlalchemy.settings import create_sqlalchemy_config
from app.exceptions import Error
from app.settings import load_settings

from litestar import Litestar
from litestar.config.compression import CompressionConfig
from litestar.config.response_cache import (
    ResponseCacheConfig,
    default_cache_key_builder,
)
from litestar.di import Provide
from litestar.plugins import PluginProtocol
from litestar.repository.exceptions import RepositoryError
from litestar.types import ControllerRouterHandler, Middleware
from msgspec import Struct
from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape, from_shape
from shapely import to_geojson
from shapely.geometry import shape as shapely_shape
from litestar.openapi.spec import Schema
from litestar.plugins import OpenAPISchemaPlugin
from litestar.typing import FieldDefinition
from litestar.openapi.spec.enums import OpenAPIType

if t.TYPE_CHECKING:
    from litestar import Request


LifespanContextManager = t.Union[
    t.Callable[[Litestar], AbstractAsyncContextManager],
    AbstractAsyncContextManager,
]


SETTINGS_DEPENDENCY_KEY = "settings"
FILTERS_DEPENDENCY_KEY = "filters"
CREATED_FILTER_DEPENDENCY_KEY = "created_filter"
ID_FILTER_DEPENDENCY_KEY = "id_filter"
LIMIT_OFFSET_DEPENDENCY_KEY = "limit_offset"
UPDATED_FILTER_DEPENDENCY_KEY = "updated_filter"
ORDER_BY_DEPENDENCY_KEY = "order_by"
SEARCH_FILTER_DEPENDENCY_KEY = "search_filter"



def enc_hook(obj: t.Any) -> t.Any:
    """Given an object that msgspec doesn't know how to serialize by
    default, convert it into an object that it does know how to
    serialize"""
    """ if not isinstance(obj, WKBElement):
        raise NotImplementedError() """
    return msgspec.json.decode(to_geojson(to_shape(obj)))


def dec_hook(type: t.Type, obj: t.Any) -> t.Any:
    """Given a type in a schema, convert ``obj`` (composed of natively
    supported objects) into an object of type ``type``.

    Any `TypeError` or `ValueError` exceptions raised by this method will
    be considered "user facing" and converted into a `ValidationError` with
    additional context. All other exceptions will be raised directly.
    """
    return from_shape(shapely_shape(obj), srid=4326)



def decode_wkb_element(value: t.Any) -> dict:
    if value is None:
        return {}
    if isinstance(value, WKBElement):
        return msgspec.json.decode(to_geojson(to_shape(value)))
    return dict(t.cast(t.Any, value))


def encode_wkb_element(value: t.Any, *, srid: int = 4326) -> WKBElement | None:
    """Convert GeoJSON-ish input into a GeoAlchemy ``WKBElement`` for persistence.

    Accepts:
    - ``None`` / empty dict -> ``None``
    - existing ``WKBElement`` -> passthrough
    - GeoJSON mapping (e.g. {"type": "...", "coordinates": ...}) -> ``WKBElement``
    - objects with ``__geo_interface__`` (e.g. Shapely geometry) -> ``WKBElement``
    """
    if value is None:
        return None
    if isinstance(value, WKBElement):
        return value
    if isinstance(value, dict):
        if not value:
            return None
        return from_shape(shapely_shape(value), srid=srid)
    if hasattr(value, "__geo_interface__"):
        return from_shape(shapely_shape(t.cast(t.Any, value).__geo_interface__), srid=srid)
    msg = f"Unsupported geometry value type for WKBElement encoding: {type(value)!r}"
    raise TypeError(msg)


class WKBElementSchemaPlugin(OpenAPISchemaPlugin):
    @staticmethod
    def is_plugin_supported_field(field_definition: FieldDefinition) -> bool:
        ann = field_definition.annotation
        return isinstance(ann, type) and issubclass(ann, WKBElement)


    def to_openapi_schema(self, field_definition: FieldDefinition, schema_creator: t.Any) -> Schema:
        # Adjust this to match what your enc_hook produces
        return Schema(
            title="GeoJSON",
            type=OpenAPIType.OBJECT,
            description="GeoJSON representation of a geometry.",
            # e.g. if you output base64 bytes as a string, you might use:
            # format="byte",
        )


class AppFactory[T: Struct]:
    def __init__(
        self,
        settings_type: type[T],
        app_settings_getter,
    ) -> None:
        self._settings = load_settings(settings_type)
        self._app_settings = app_settings_getter(self._settings)
        self._route_handlers: list[ControllerRouterHandler] = [
            HealthController,
        ]
        self._dependencies: dict[str, Provide] = {
            SETTINGS_DEPENDENCY_KEY: Provide(
                lambda: self._settings,
                sync_to_thread=False,
            ),
            LIMIT_OFFSET_DEPENDENCY_KEY: Provide(
                provide_limit_offset_pagination,
                sync_to_thread=False,
            ),
            UPDATED_FILTER_DEPENDENCY_KEY: Provide(
                provide_updated_filter,
                sync_to_thread=False,
            ),
            CREATED_FILTER_DEPENDENCY_KEY: Provide(
                provide_created_filter,
                sync_to_thread=False,
            ),
            ID_FILTER_DEPENDENCY_KEY: Provide(
                provide_id_filter,
                sync_to_thread=False,
            ),
            SEARCH_FILTER_DEPENDENCY_KEY: Provide(
                provide_search_filter,
                sync_to_thread=False,
            ),
            ORDER_BY_DEPENDENCY_KEY: Provide(
                provide_order_by,
                sync_to_thread=False,
            ),
            FILTERS_DEPENDENCY_KEY: Provide(
                provide_filter_dependencies,
                sync_to_thread=False,
            ),
        }
        self._sqla_config = create_sqlalchemy_config(self._app_settings.sqlalchemy)
        self._plugins: list[PluginProtocol] = [
            SQLAlchemyPlugin(self._sqla_config),
        ]
        self._signature_namespace: dict[str, t.Any] = {}
        self._middleware: list[Middleware] = []

        @asynccontextmanager
        async def lifespan(app: Litestar):
            yield
            #await self._redis.aclose()

        self._lifespan: list[LifespanContextManager] = [lifespan]
        self._queue_configs: list[QueueConfig] = []


    def add_route(
        self,
        route_handler: ControllerRouterHandler,
    ) -> None:
        self._route_handlers.append(route_handler)


    def add_routes(
        self,
        route_handlers: t.Iterable[ControllerRouterHandler],
    ) -> None:
        self._route_handlers.extend(route_handlers)


    def add_dependency(self, key: str, dependency: Provide) -> None:
        self._dependencies[key] = dependency


    def add_dependencies(self, dependencies: t.Mapping[str, Provide]) -> None:
        self._dependencies.update(dependencies)


    def add_lifespan(self, lifespan: LifespanContextManager) -> None:
        self._lifespan.append(lifespan)


    def add_plugin(self, plugin: PluginProtocol) -> None:
        self._plugins.append(plugin)


    def add_plugins(self, plugins: t.Iterable[PluginProtocol]) -> None:
        self._plugins.extend(plugins)


    def add_type(self, key: str, value: t.Any) -> None:
        self._signature_namespace[key] = value


    def add_types(self, types: t.Mapping[str, t.Any]) -> None:
        self._signature_namespace.update(types)


    def add_queue(self, config: QueueConfig) -> None:
        self._queue_configs.append(config)


    def add_queues(self, configs: t.Iterable[QueueConfig]) -> None:
        self._queue_configs.extend(configs)

    
    def add_middleware(self, middleware: Middleware) -> None:
        self._middleware.append(middleware)


    def cache_key_builder(self, request: Request) -> str:
        default_key = default_cache_key_builder(request)
        return f"{self._app_settings.api.app_name}:{default_key}"


    def create_settings_getter(self) -> t.Callable[[], T]:
        return lambda: self._settings


    def create_session_getter(self):
        return lambda: self._sqla_config.get_session()


    def create_app(self) -> Litestar:
        return Litestar(
            debug=self._app_settings.api.debug,
            cors_config=create_cors_config(self._app_settings.api),
            compression_config=CompressionConfig(
                backend="brotli",
                exclude=["/saq"],
            ),
            openapi_config=create_openapi_config(self._app_settings),
            plugins=self._plugins + [
                create_saq_plugin(
                    settings=self._app_settings.saq,
                    queue_configs=self._queue_configs,
                ),
                WKBElementSchemaPlugin(),
            ],
            route_handlers=self._route_handlers,
            exception_handlers={
                Error: exception_handler,
                RepositoryError: exception_handler,
            },
            dependencies=self._dependencies,
            lifespan=self._lifespan,
            response_cache_config=ResponseCacheConfig(
                default_expiration=self._app_settings.api.cache_expiration,
                key_builder=self.cache_key_builder,
            ),
            signature_namespace=self._signature_namespace,
            middleware=self._middleware,
            type_encoders={
                WKBElement: enc_hook,
            },
            type_decoders=[
                (lambda t: t is WKBElement, dec_hook)
            ],
        )
