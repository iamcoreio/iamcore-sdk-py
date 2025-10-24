# IAM Core Python SDK

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/pypi/v/iamcore-sdk-py.svg)](https://pypi.org/project/iamcore-sdk-py/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A comprehensive Python SDK for interacting with IAM Core, a powerful identity and access management platform. This SDK provides a clean, type-safe interface for managing users, tenants, applications, policies, and other IAM resources.

## ✨ Features

- **Type-Safe**: Full type hints and Pydantic models for reliable development
- **Comprehensive**: Support for all IAM Core resources (users, tenants, applications, policies, etc.)
- **Easy to Use**: Simple, intuitive API with clear method names
- **Well Tested**: High test coverage with comprehensive unit tests
- **Production Ready**: Robust error handling and timeout management

## 🚀 Installation

Install the SDK using pip:

```bash
pip install iamcore-sdk-py
```

Or using uv (recommended):

```bash
uv add iamcore-sdk-py
```

## 📋 Requirements

- Python 3.9+
- Dependencies are automatically managed

## 🏁 Quick Start

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
config.set_iamcore_config(
    iamcore_url="https://your-iam-core-instance.com",
    iamcore_issuer_url="https://your-issuer.com",
    client_id="your-client-id"
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
# Authenticate and get tokens
auth_response = iam_client.auth.authenticate(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Use the access token for subsequent requests
headers = {"Authorization": f"Bearer {auth_response.access_token}"}
```

### 4. Use the API

Now you can interact with IAM Core resources:

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

## 📚 Available Clients

The SDK provides clients for all major IAM Core resources:

### 🔐 Authentication (`iam_client.auth`)
- User authentication and token management

### 👥 Users (`iam_client.user`)
- Create, read, update, delete users
- User search and filtering
- User group management
- Policy attachment

### 🏢 Tenants (`iam_client.tenant`)
- Tenant management
- Tenant issuer configuration
- Multi-tenant operations

### 📱 Applications (`iam_client.application`)
- Application lifecycle management
- Application search and filtering
- Policy attachment to applications

### 🔑 API Keys (`iam_client.api_key`)
- API key creation and management
- Key retrieval and pagination

### 👥 Groups (`iam_client.group`)
- Group management
- User-group associations

### 📋 Policies (`iam_client.policy`)
- Policy CRUD operations
- Policy attachment to resources

### 🔍 Resources (`iam_client.resource`)
- Resource management
- Resource search and filtering

### ⚡ Evaluation (`iam_client.evaluate`)
- Policy evaluation against resources

### 📊 Application Resource Types (`iam_client.application_resource_type`)
- Application resource type management

## 💡 Usage Examples

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

app_filter = ApplicationSearchFilter(name="my-app")
apps = iam_client.application.search_application(headers, app_filter)

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

## 🔧 Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/your-org/iamcore-sdk-py.git
cd iamcore-sdk-py

# Install dependencies with uv
uv sync --dev

# Run tests
pytest

# Run linting
ruff check .

# Run type checking
pyright .
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov --cov-report html

# Run specific test file
pytest tests/unit/clients/test_user_client.py

# Run tests matching pattern
pytest -k "test_create"
```

### Code Quality

This project uses:
- **ruff** for linting and formatting
- **pyright** for type checking
- **pytest** for testing
- **pre-commit** hooks for quality gates

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📖 API Documentation

For detailed API documentation, see the [IAM Core API Documentation](https://iamcore-api-docs.vercel.app).

## 🐛 Issues & Support

- **Bug Reports**: [GitHub Issues](https://github.com/your-org/iamcore-sdk-py/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/iamcore-sdk-py/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ by the IAM Core team
- Thanks to all contributors and the open-source community

---

**Happy coding with IAM Core! 🚀**