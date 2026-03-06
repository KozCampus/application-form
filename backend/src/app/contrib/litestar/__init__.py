from __future__ import annotations

import typing as t

from advanced_alchemy.filters import FilterTypes, LimitOffset, BeforeAfter, OnBeforeAfter
from advanced_alchemy.repository import (
    SQLAlchemyAsyncRepository,
    SQLAlchemyAsyncQueryRepository,
)
from advanced_alchemy.service import OffsetPagination
from litestar_saq import CronJob, QueueConfig, TaskQueues
from saq.job import Job, Status
from saq.types import Context, QueueInfo
from sqlalchemy.ext.asyncio import AsyncSession
from app.contrib.litestar.dependencies import *  # type: ignore
from app.contrib.litestar.factory import AppFactory
from app.contrib.litestar.settings import AppSettings

from litestar import (
    Request,
    Response,
    Controller,
    delete,
    get,
    patch,
    post,
    put,
)
from litestar.di import Provide
from litestar.enums import RequestEncodingType
from litestar.params import Body, Dependency, Parameter
from litestar.types import ControllerRouterHandler
from litestar.response import Redirect
from litestar.background_tasks import BackgroundTask, BackgroundTasks


__all__ = [
    "t",
    "Request",
    "Response",
    "Controller",
    "Redirect",
    "get",
    "post",
    "put",
    "patch",
    "delete",
    "Provide",
    "Parameter",
    "Dependency",
    "Body",
    "ControllerRouterHandler",
    "RequestEncodingType",
    "LimitOffset",
    "FilterTypes",
    "BeforeAfter",
    "OnBeforeAfter",
    "SQLAlchemyAsyncRepository",
    "SQLAlchemyAsyncQueryRepository",
    "SQLAlchemyAsyncRepositoryService",
    "OffsetPagination",
    "AsyncSession",
    "Job",
    "Status",
    "Context",
    "QueueInfo",
    "QueueConfig",
    "TaskQueues",
    "CronJob",
    "AppSettings",
    "AppFactory",
    "provide_id_filter",
    "provide_limit_offset_pagination",
    "provide_updated_filter",
    "provide_created_filter",
    "provide_order_by",
    "provide_search_filter",
    "provide_filter_dependencies",
    "create_service_provider",
    "BackgroundTask",
    "BackgroundTasks",
]
