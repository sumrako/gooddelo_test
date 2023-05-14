import logging

import uvicorn
from fastapi import FastAPI

from app.routes import router
from app.settings import settings

app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.ALLOWED_HOST,
        port=settings.ALLOWED_PORT,
        reload=True,
        log_level=logging.INFO,
        use_colors=True
    )
