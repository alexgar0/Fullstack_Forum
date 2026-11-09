import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from forum.core.config import settings
from forum.core.exceptions import register_exception_handlers
from forum.core.log import initialize_logger
from forum.features.branch.view import router as branch_router
from forum.features.reply.view import router as reply_router
from forum.features.topic.view import router as topic_router
from forum.features.user.view import router as user_router

app = FastAPI(
    title="Forum API",
    description="Forum API",
    version="0.1.0",
)
register_exception_handlers(app)

app.include_router(user_router)
app.include_router(topic_router)
app.include_router(branch_router)
app.include_router(reply_router)


@app.get("/", response_model=None)
async def root() -> JSONResponse:
    return JSONResponse({"message": "Welcome to Forum API!"})


def main() -> None:
    initialize_logger()
    if settings.dev:
        uvicorn.run("forum.core.main:app", host="0.0.0.0", port=8080, reload=True)  # noqa: S104
    else:
        uvicorn.run(app, host="0.0.0.0", port=8080)  # noqa: S104


if __name__ == "__main__":
    main()
