import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres_user:password@localhost:5432/postgres_db"
)
SECRET_KEY = os.getenv(
    "SECRET_KEY", "03a0e4d297086a50fd853f8b0067432aade9b4b2a9f98c123d3da387b2e2ae5a"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

USERNAME_LENGTH_BOUNDS = (4, 15)
BRANCH_NAME_LENGTH_BOUNDS = (2, 30)
TOPIC_TITLE_LENGTH_BOUNDS = (5, 60)
TOPIC_EDITION_TIMEFRAME_MINUTES = 30
