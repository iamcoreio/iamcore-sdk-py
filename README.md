# IAM Core Python SDK

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/pypi/v/iamcore-sdk-py.svg)](https://pypi.org/project/iamcore-sdk-py/)

A comprehensive Python SDK for interacting with IAMCore. This SDK provides interface for managing users, tenants, applications, policies, and other IAM resources.

## Installation

Install the SDK using pip:

```bash
pip install iamcore-sdk-py
```

Or using uv (recommended):

```bash
uv add iamcore-sdk-py
```

## Requirements

- Python 3.9+
- Dependencies are automatically managed

## Quick Start

### 1. Configuration

First, configure your IAM Core connection:

```python
from iamcore.client.config import BaseConfig

# Option 1: Environment variables (recommended)
# Set these in your environment or .env file:
# IAMCORE_URL=https://your-iam-core-instance.com
# IAMCORE_ISSUER_URL=https://your-issuer.com
# SYSTEM_BACKEND_CLIENT_ID=your-client-id
# IAMCORE_CLIENT_TIMEOUT=30

config = BaseConfig()

# Option 2: Manual configuration
config = BaseConfig(
    iamcore_url="https://your-iam-core-instance.com",
    iamcore_issuer_url="https://your-issuer.com",
    system_backend_client_id="your-client-id",
    iamcore_client_timeout=30
)
```

### 2. Initialize the Client

```python
from iamcore.client import Client

# Create the main client
iam_client = Client(config)
```

### 3. Authentication

Authenticate to get access tokens:

```python
# Authenticate and get tokens using password grant
token = iam_client.auth.get_token_with_password(
    realm="your-tenant-realm",
    client_id="your-client-id",
    username="your-username",
    password="your-password"
)

# Use the access token for subsequent requests
headers = token.access_headers
```

### 4. Use the API

Now you can interact with IAM Core API:

```python
# Get current user information
current_user = iam_client.user.get_user_me(headers)
print(f"Hello, {current_user.first_name} {current_user.last_name}!")

# List tenants
tenants = iam_client.tenant.search_tenants(headers)
for tenant in tenants.data:
    print(f"Tenant: {tenant.name}")

# Create a new user
from iamcore.client.user.dto import CreateUser

new_user_data = CreateUser(
    email="john.doe@example.com",
    username="johndoe",
    password="secure-password",
    confirm_password="secure-password",
    first_name="John",
    last_name="Doe"
)

created_user = iam_client.user.create_user(headers, new_user_data)
print(f"Created user: {created_user.username}")
```

## Available Clients

The SDK provides clients for all major IAM Core resources:

### Authentication (`iam_client.auth`)

- User authentication and token management

### Users (`iam_client.user`)

- Create, read, update, delete users
- User search and filtering
- User group management
- Policy attachment

### Tenants (`iam_client.tenant`)

- Tenant management
- Tenant issuer configuration
- Multi-tenant operations

### Applications (`iam_client.application`)

- Application lifecycle management
- Application search and filtering
- Policy attachment to applications

### API Keys (`iam_client.api_key`)

- API key creation and management
- Key retrieval and pagination

### Groups (`iam_client.group`)

- Group management
- User-group associations

### Policies (`iam_client.policy`)

- Policy CRUD operations
- Policy attachment to resources

### Resources (`iam_client.resource`)

- Resource management
- Resource search and filtering

### Evaluation (`iam_client.evaluate`)

- Policy evaluation against resources

### Application Resource Types (`iam_client.application_resource_type`)

- Application resource type management

## Usage Examples

### Managing Users

```python
# Search users with filters
from iamcore.client.user.dto import UserSearchFilter

user_filter = UserSearchFilter(
    email="example.com",
    first_name="John"
)

users = iam_client.user.search_users(headers, user_filter)
for user in users.data:
    print(f"User: {user.username} - {user.email}")

# Update user information
from iamcore.client.user.dto import UpdateUser

update_data = UpdateUser(
    first_name="Johnny",
    email="johnny.doe@example.com"
)

iam_client.user.update_user(headers, user.irn, update_data)

# Attach policies to user
iam_client.user.user_attach_policies(headers, user.irn, ["policy-id-1", "policy-id-2"])
```

### Working with Applications

```python
# Create a new application
from iamcore.client.application.dto import CreateApplication

app_data = CreateApplication(
    name="my-awesome-app",
    display_name="My Awesome Application"
)

new_app = iam_client.application.create_application(headers, app_data)

# Search applications
from iamcore.client.application.dto import ApplicationSearchFilter

application_filter = ApplicationSearchFilter(name="my-app")
apps = iam_client.application.search_application(headers, application_filter)

# Attach policies to application
iam_client.application.application_attach_policies(
    headers,
    new_app.irn,
    ["read-policy", "write-policy"]
)
```

### Tenant Management

```python
# Get all tenants with pagination
tenants = iam_client.tenant.search_tenants(headers)

# Create a new tenant
from iamcore.client.tenant.dto import CreateTenant

tenant_data = CreateTenant(
    name="new-tenant",
    display_name="New Tenant Organization"
)

new_tenant = iam_client.tenant.create_tenant(headers, tenant_data)
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/your-org/iamcore-sdk-py.git
cd iamcore-sdk-py

# Install dependencies with uv
uv sync --dev

# Run tests
uv run pytest

# Run linting
ruff check . --fix

# Run type checking
pyright .
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov --cov-report html

# Run specific test file
uv run pytest tests/unit/clients/test_user_client.py

# Run tests matching pattern
uv run pytest -k "test_create"
```

### Code Quality

This project uses:

- **ruff** for linting and formatting
- **pyright** for type checking
- **pytest** for testing
- **pre-commit** hooks for quality gates
