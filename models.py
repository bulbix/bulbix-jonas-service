from pydantic import BaseModel


class JonasBook(BaseModel):
    number: int
    title: str
    author: str
    sold: bool
    level: int
    section: str

