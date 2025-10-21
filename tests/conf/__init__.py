from __future__ import annotations

import os

IAMCORE_ROOT_USER: str = os.getenv("IAMCORE_ROOT_USER", "iamcore")
IAMCORE_ROOT_PASSWORD: str | None = os.getenv("IAMCORE_ROOT_PASSWORD")
