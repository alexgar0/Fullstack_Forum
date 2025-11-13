import logging
from time import sleep
from fastapi import FastAPI
import uvicorn
from src.user.view import router as user_router
from src.log import initialize_logger

app = FastAPI(
    title="Forum API",
    description="Forum API",
    version="0.1.0",
)
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Forum API!"}

def main():
    initialize_logger()
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
