from __future__ import annotations

import typing as t
from datetime import date, datetime, time
from uuid import UUID

from advanced_alchemy.base import (
    DefaultBase as _DefaultBase,
)
from advanced_alchemy.base import (
    UUIDAuditBase as _UUIDAuditBase,
)
from advanced_alchemy.base import (
    UUIDBase as _UUIDBase,
)
from app.contrib.sqlalchemy.engine import create_engine
from app.contrib.sqlalchemy.settings import SQLAlchemySettings

from sqlalchemy import JSON, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship, 
    MappedSQLExpression,
    column_property,
    query_expression,
)
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from geoalchemy2 import Geometry, WKBElement
from sqlalchemy.inspection import inspect as sa_inspect
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import literal_column


class _TypeAnnotationMixin:
    __abstract__ = True

    type_annotation_map = {
        str: String,
        t.Any: JSON().with_variant(JSONB, "postgresql"),
    }


class DefaultBase(_DefaultBase, _TypeAnnotationMixin):
    __abstract__ = True


class UUIDBase(_UUIDBase, _TypeAnnotationMixin):
    __abstract__ = True


class UUIDAuditBase(_UUIDAuditBase, _TypeAnnotationMixin):
    __abstract__ = True


def update(db_obj, data):
    for key in data.__annotations__.keys():
        value = getattr(data, key)
        setattr(db_obj, key, value)


__all__ = [
    "t",
    "UUID",
    "date",
    "datetime",
    "time",
    "DefaultBase",
    "UUIDBase",
    "UUIDAuditBase",
    "Mapped",
    "mapped_column",
    "relationship",
    "UniqueConstraint",
    "String",
    "Text",
    "JSON",
    "ForeignKey",
    "JSONB",
    "ENUM",
    "SQLAlchemySettings",
    "create_engine",
    "update",
    "AssociationProxy",
    "association_proxy",
    "Geometry",
    "WKBElement",
    "hybrid_property",
    "column_property",
    "literal_column",
    "MappedSQLExpression",
    "query_expression",
]
