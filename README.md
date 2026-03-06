# közcampus

A web application skeleton based on a SvelteKit frontend and a Python/Litestar backend.

> For setup instructions, consult the `README.md` in the `backend` and `frontend` directories.

## Architecture

### Backend

Python ASGI application using:
- [Litestar](https://litestar.dev/) web framework
- PostgreSQL with [PostGIS](https://postgis.net/) extension
- [SQLAlchemy](https://www.sqlalchemy.org/) ORM with [Advanced Alchemy](https://docs.advanced-alchemy.litestar.dev/latest/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) for migrations
- OAuth2 SSO via Google
- [msgspec](https://jcristharif.com/msgspec/) for serialization

### Frontend

SvelteKit application using:
- [Tailwind CSS v4](https://tailwindcss.com/) for styling
- [shadcn-svelte](https://www.shadcn-svelte.com/) UI components
- [Axios](https://axios-http.com/) for API requests

### Domain structure

| Context    | Entities     | Type |
| ---------- | ------------ | ---- |
| Volunteers | Account      | core |
