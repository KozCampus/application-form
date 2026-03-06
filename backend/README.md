# közcampus — backend

A Python ASGI application using:

- [Litestar](https://litestar.dev/) web framework
- PostgreSQL with [PostGIS](https://postgis.net/) extension
- [SQLAlchemy](https://www.sqlalchemy.org/) ORM
- [Advanced Alchemy](https://docs.advanced-alchemy.litestar.dev/latest/) for the repository and service layers
- [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/en/latest/index.html) for geospatial data support
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) database migration tool
- OAuth2 SSO with [Google](https://console.cloud.google.com)
- [msgspec](https://jcristharif.com/msgspec/) for serialization and validation

## Development setup

### Installation

1. Make sure the following prerequisites are installed.

- `python` (version 3.12 or higher)
- `poetry` ([installation](https://python-poetry.org/docs/))

2. Clone the repository and enter the backend directory.

3. Install the dependencies.

```bash
poetry install
```

### Configuring the application

1. Copy the configuration file template.

```bash
cp config.example.toml config.toml
```

2. Edit `config.toml`. The values `sqlalchemy.db.url`, `sso.google.client_id` and `sso.google.client_secret` must be set.

### Running the application

1. Activate the virtual environment.

```bash
$(poetry env activate)
```

2. Start the development server.

```bash
app run --reload
```

> The API documentation is available at `http://localhost:8000/schema`.
