from __future__ import annotations

from app.server import factory
from app.server.routes import get_routes
from app.server.dependencies import get_dependencies


__all__ = [
    "app",
]


routes = get_routes()
factory.add_routes(routes)

dependencies = get_dependencies()
factory.add_dependencies(dependencies)

app = factory.create_app()
