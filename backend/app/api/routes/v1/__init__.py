from fastapi import APIRouter

from app.api.routes.v1.statements import router as statements_router

router = APIRouter(prefix="/v1")
router.include_router(statements_router)