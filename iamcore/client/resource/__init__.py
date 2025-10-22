from .client import (
    create_resource,
    delete_resource,
    delete_resources,
    search_all_resources,
    search_resource,
    update_resource,
)
from .dto import Resource

__all__ = [
    "Resource",
    "create_resource",
    "delete_resource",
    "delete_resources",
    "search_all_resources",
    "search_resource",
    "update_resource",
]
