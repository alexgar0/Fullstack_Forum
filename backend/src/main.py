import logging
from time import sleep
from fastapi import FastAPI
import uvicorn
from .features.user.view import router as user_router
from .features.topic.view import router as topic_router
from .features.branch.view import router as branch_router
from .log import initialize_logger
from .exceptions import register_exception_handlers

app = FastAPI(
    title="Forum API",
    description="Forum API",
    version="0.1.0",
)
register_exception_handlers(app)

app.include_router(user_router)
app.include_router(topic_router)
app.include_router(branch_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Forum API!"}

def main():
    initialize_logger()
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
