from fastapi import APIRouter
from .v1.auth.router import router as auth_router
from .v1.receipt.router import router as receipt_router

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(receipt_router, prefix="/receipt", tags=["Receipt"])
