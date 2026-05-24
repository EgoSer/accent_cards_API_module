from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from .auth import auth_router
from .meta import description, module_name, module_tags, prefix, version

router = APIRouter(prefix=prefix, tags=module_tags)
router.include_router(auth_router)


@router.get("/")
def root():
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"module": module_name, "description": description, "version": version}
    )
