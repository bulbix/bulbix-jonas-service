from pydantic import BaseModel
from typing import Dict


class JonasBook(BaseModel):
    number: int
    title: str
    author: str
    sold: bool
    level: int
    section: str
    isbndb: Dict
