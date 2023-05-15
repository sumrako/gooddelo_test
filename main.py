import logging

import uvicorn
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.routes import router
from app.settings import settings
from auth.api import limiter

app = FastAPI()
app.include_router(router)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.ALLOWED_HOST,
        port=settings.ALLOWED_PORT,
        reload=True,
        log_level=logging.INFO,
        use_colors=True
    )
