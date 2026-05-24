from enum import Enum

module_tags: list[str | Enum] | None  # required for automatic importing

# Metadata used by module

module_name = "Admin panel"  # The name of your module
version = "0.1.0-pre-alpha"  # Actual version of your module
description = "A collection of admin panel backend endpoints"  # description of your module
prefix = "/admin"  # prefix is used by fastapi Router class to define how to access your module
module_tags = [module_name]  # Swagger (openAPI) section for this module
