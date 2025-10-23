# Agent Guidelines for iamcore-sdk-py

This document outlines the conventions and commands for agentic coding in this repository.

## 1. Build/Lint/Test Commands

*   **Install Dependencies**: `uv sync --dev`
*   **Run All Tests**: `pytest --cov --cov-report term --cov-report xml:coverage.xml`
*   **Run a Single Test**: `pytest <path_to_test_file>::<test_function_name>`
*   **Lint Code**: `ruff check .`
*   **Auto-fix Lint Issues**: `ruff check . --fix`
*   **Type Check (Pyright)**: `pyright .`
*   **Type Check (MyPy)**: `mypy .`

## 2. Code Style Guidelines

*   **Imports**: Follow `isort` conventions (handled by `ruff`). Imports should be grouped and sorted.
*   **Formatting**: Adhere to a line length of 120 characters. `ruff` handles most formatting.
*   **Types**: Strict type hinting is enforced by `pyright` and `mypy`. Use type hints consistently.
*   **Naming**: Follow PEP 8 naming conventions (e.g., `snake_case` for functions/variables, `CamelCase` for classes).
*   **Error Handling**: Use standard Python `try...except` blocks for error handling.
*   **Docstrings**: While not strictly enforced by a specific linter rule, aim for clear and concise docstrings for public API elements.

## 3. Cursor/Copilot Rules

No specific Cursor or Copilot rules were found in the repository.
