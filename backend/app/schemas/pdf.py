from pydantic import BaseModel


class PageResult(BaseModel):
    page: int
    text: str


class ParseResponse(BaseModel):
    filename: str
    total_pages: int
    pages: list[PageResult]
