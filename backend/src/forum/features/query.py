from pydantic import BaseModel


class PaginationQuery(BaseModel):
    page: int = 1
    limit: int = 30
