from fastapi import APIRouter
from auth.api import router as auth

router = APIRouter()
router.include_router(auth)

