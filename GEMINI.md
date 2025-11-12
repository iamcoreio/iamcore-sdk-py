# Project: iamcore-sdk-py

## Project Overview

This project is a Python SDK for interacting with IAM Core APIs. It provides client classes for various IAM Core services, including API key, application, application resource type, authentication, evaluation, group, policy, resource, tenant, and user management. The SDK leverages `pydantic` for data transfer objects (DTOs) and `requests` for HTTP communication.

## Technologies Used

- **Language**: Python 3.9
- **Dependency Management**: `uv`
- **Data Validation**: `pydantic`
- **HTTP Client**: `requests`
- **Type Checking**: `pyright`, `mypy`
- **Linting & Formatting**: `ruff`
- **Testing**: `pytest`, `pytest-cov`, `pytest-benchmark`, `pytest-mock`

## Building and Running

### Install Dependencies

```bash
uv sync --dev
```

### Running Tests

- **Run All Tests**:
  ```bash
  uv run pytest --cov --cov-report term --cov-report xml:coverage.xml
  ```
- **Run a Single Test**:
  ```bash
  uv run pytest <path_to_test_file>::<test_function_name>
  ```

### Linting and Type Checking

- **Lint Code**:
  ```bash
  ruff check .
  ```
- **Auto-fix Lint Issues**:
  ```bash
  ruff check . --fix
  ```
- **Type Check (Pyright)**:
  ```bash
  pyright .
  ```
- **Type Check (MyPy)**:
  ```bash
  mypy .
  ```

## Development Conventions

- **Code Style**: Adheres to `isort` conventions for imports, 120-character line length, and PEP 8 naming conventions.
- **Type Hinting**: Strict type hinting is enforced using `pyright` and `mypy`.
- **Error Handling**: Standard Python `try...except` blocks are used for error handling.
- **Docstrings**: Clear and concise docstrings are encouraged for public API elements.
- **Testing**: Comprehensive unit and integration tests are implemented using `pytest`, aiming for 80% overall code coverage. Mocking is used for external API calls.
