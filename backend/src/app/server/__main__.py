from __future__ import annotations

from app.cli import create_cli


cli = create_cli("app.server.asgi:app")


if __name__ == "__main__":
    cli()
