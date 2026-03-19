from pydantic import BaseModel


class PaginationQuery(BaseModel):
    offset: int = 0
    limit: int = 30
