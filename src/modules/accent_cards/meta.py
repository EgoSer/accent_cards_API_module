from enum import Enum

module_tags: list[str | Enum] | None  # required for automatic importing

# Metadata used by module

module_name = "Accent cards"  # The name of your module
version = "0.1a"  # Actual version of your module
prefix = "/cards/accent"  # prefix is used by fastapi Router class to define how to access your module
module_tags = ["accent"]
