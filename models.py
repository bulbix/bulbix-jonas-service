from pydantic import BaseModel
from typing import Dict, Union


class JonasBook(BaseModel):
    uuid: str
    number: int
    title: str
    author: str
    sold: bool
    level: int
    section: str
    isbndb: Dict


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str
