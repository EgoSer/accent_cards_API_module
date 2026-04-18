import importlib
import pkgutil
from pathlib import Path

from fastapi import FastAPI
from loguru import logger


def register_modules(app: FastAPI):
    modules_path = Path(__file__).parent
    logger.info(f"Initialised module loading from directory {modules_path}")
    for module_info in pkgutil.iter_modules([modules_path]):
        if module_info.name.startswith("_"):
            continue
        try:
            module = importlib.import_module(f".{module_info.name}", package=__package__)
            logger.info(module.__dir__())
            if hasattr(module, "router"):
                app.include_router(module.router)
            if hasattr(module, "meta"):
                logger.info(f"Loaded module {module.module_name}")
        except Exception as e:
            logger.error(f"Couldn't import module {module_info.name}: {e}")

    logger.info("Module loading finished")
