# Agent Instructions

## Run Commands

```bash
# Run the API
uv run bill-splitter-api

# Run in development mode
uv run fastapi dev
```

## Database Migrations

Alembic is configured. Run migrations after any model changes.

```bash
# Create new migration
uv run alembic revision --autogenerate -m "description"

# Apply all migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# Check current version
uv run alembic current
```

## Linting

```bash
uv add ruff
uv run ruff check src/
```

## Project Structure

- Entry point: `src/bill_splitter_api.main:app`
- All source code: `src/bill_splitter_api/`
- Models: `src/bill_splitter_api/models/`
- Routes: `src/bill_splitter_api/*/routes.py`
- Schemas: `src/bill_splitter_api/*/schemas.py`

## Configuration

Environment variables use `__` delimiter for nesting:

```
JWT__SECRET_KEY=...
JWT__ALGORITHM=HS256
DB__USER=postgres
DB__PASSWORD=postgres
DB__NAME=bill_splitter
DB__HOST=localhost
DB__PORT=5432
```

## Model Notes

- Models use `ModelBase` which auto-generates `uuid.uuid7()` for `id` in `__init__`.
- Pass `id=...` to the constructor to override.

## Testing

- No test files exist in this repository.
- No mypy configuration.
