from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from forum.database import get_db

DatabaseDep = Annotated[Session, Depends(get_db)]
