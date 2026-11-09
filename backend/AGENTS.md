# AGENTS.md

## Project Overview

This is a Python backend application built with FastAPI, SQLAlchemy, Pydantic v2, and PostgreSQL.

The project follows a feature-based modular architecture with explicit separation of API, business logic, and persistence.

## Technology Stack

- Python 3.13+
- FastAPI
- SQLAlchemy 2.x
- Pydantic v2
- PostgreSQL
- Alembic
- uv for dependency management
- Ruff for linting and formatting
- mypy for static type checking
- pytest for testing

## General Principles

- Prefer simplicity over unnecessary abstractions.
- Follow existing project conventions before introducing new patterns.
- Write maintainable, readable, and type-safe Python code.
- Avoid premature optimization.
- Do not introduce dependencies without clear justification.
- Do not modify unrelated code.
- Do not create abstractions for a single use case without a concrete reason.
- Prefer standard library functionality when appropriate.

## Architecture

Follow the existing feature-based project structure.

Each feature may contain:

- `view.py` — HTTP endpoints and request handling.
- `service.py` — business logic and orchestration.
- `repo.py` — database access.
- `schemas.py` — Pydantic DTOs.
- `models.py` — SQLAlchemy ORM models.
- `dependencies.py` — FastAPI dependencies.

Rules:

- Keep route handlers thin.
- Business logic belongs in services.
- Database queries belong in repositories.
- Services must not depend on FastAPI request or response objects.
- Repositories must not contain business logic.
- Use dependency injection for services and repositories.
- Do not introduce circular dependencies.
- Avoid leaking ORM models into public API contracts.
- Preserve established transaction boundaries.
- Use `.agent-venv` as main venv.

## Python Coding Standards

- Use modern Python syntax.
- Use built-in generics: `list[str]`, `dict[str, int]`.
- Use union syntax: `str | None`.
- Prefer Python 3.12+ generic syntax where appropriate.
- Use type annotations for public functions and methods.
- Prefer explicit, descriptive names.
- Follow Ruff configuration from `pyproject.toml`.
- Do not add unnecessary comments.
- Write docstrings for non-obvious behavior.

## FastAPI

- Use `Annotated` for dependency injection.
- Keep dependencies in dedicated modules when reusable.
- Use Pydantic models for request and response validation.
- Raise domain exceptions from services.
- Translate domain exceptions into HTTP responses at the API boundary.
- Do not raise `HTTPException` inside business services.
- Use appropriate HTTP status codes.

## SQLAlchemy

- Use SQLAlchemy 2.x typed ORM mappings.
- Prefer `Mapped` and `mapped_column`.
- Avoid unnecessary database queries.
- Prevent N+1 query problems.
- Use explicit transaction boundaries.
- Do not commit transactions implicitly inside generic repositories.
- Do not introduce schema changes without an Alembic migration.

## Pydantic

- Use Pydantic v2 APIs.
- Use `ConfigDict(from_attributes=True)` for ORM-compatible DTOs.
- Use `Field(default_factory=...)` for mutable defaults when needed.
- Keep business logic out of DTOs.
- Use validators only for data validation and normalization.

## Error Handling

- Define domain-specific exceptions for business failures.
- Do not silently swallow exceptions.
- Avoid broad `except Exception` unless required at an explicit boundary.
- Preserve original exception context.
- Never expose secrets or internal exception details in API responses.

## Testing

- Write tests for new business logic.
- Update existing tests when behavior changes.
- Prefer pytest fixtures over duplicated setup.
- Mock external services at integration boundaries.
- Test expected behavior, edge cases, and failures.
- Do not modify tests merely to hide implementation defects.

## Commands

Install dependencies:

```bash
uv sync --all-groups
```

Run tests:

```bash
uv run pytest
```

Lint:

```bash
uv run ruff check .
```

Format:

```bash
uv run ruff format .
```

Type checking:

```bash
uv run mypy src
```

## Security

- Never hardcode credentials or secrets.
- Never commit `.env` files containing secrets.
- Validate untrusted input at system boundaries.
- Avoid logging passwords, tokens, or sensitive information.
- Do not weaken authentication or authorization checks.

## Agent Workflow

Before making changes:

1. Inspect relevant files and existing conventions.
2. Understand dependencies and affected components.
3. Identify the smallest safe implementation.
4. Explain significant architectural changes before implementing them.

When implementing:

1. Make focused changes.
2. Preserve backward compatibility unless explicitly instructed otherwise.
3. Avoid unrelated refactoring.
4. Add or update relevant tests.
5. Follow existing formatting and naming conventions.

After making changes:

1. Run relevant tests.
2. Run Ruff checks.
3. Run type checking when applicable.
4. Review the diff for unintended changes.
5. Summarize the implementation and verification results.
6. Explicitly report checks that could not be run.

## Restrictions

- Do not delete existing tests without explicit authorization.
- Do not modify database migrations that have already been applied.
- Do not modify CI/CD configuration unless requested.
- Do not introduce new frameworks without approval.
- Do not execute destructive database commands.
- Do not commit or push changes unless explicitly requested.
- Do not ever modify README.md unless asked to do so.