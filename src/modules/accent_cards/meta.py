from enum import Enum

module_tags: list[str | Enum] | None  # required for automatic importing

# Metadata used by module

module_name = "Accent cards"  # The name of your module
version = "0.2.1-beta"  # Actual version of your module
description = (
    "Returns requested amount of accent cards (or less if database have not enough)"  # description of your module
)
prefix = "/cards/accent"  # prefix is used by fastapi Router class to define how to access your module
module_tags = ["accent"]
