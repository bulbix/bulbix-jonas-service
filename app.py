from jonasmongo import JonasMongo
from fastapi import FastAPI, Query, Body
from models import JonasBook
from typing import Optional
import requests
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jonasmongo = JonasMongo()


@app.post("/add_book")
def add_book(book: JonasBook = Body(...)):
    jonasmongo.upsert_book(book)
    return {"message": "success"}


@app.get("/search_book")
def search_book(
    title: Optional[str] = Query(None, max_length=50),
    author: Optional[str] = Query(None, max_length=50)
):
    result = jonasmongo.search_book(title, author)
    return result


@app.get("/consult_isbn")
def consult_isbn(
    isbn: Optional[str] = Query(..., min_length=1, max_length=50)
):
    h = {'Authorization': '47951_7a589993060668ed64758de54555018c'}
    resp = requests.get(f"https://api2.isbndb.com/book/{isbn}", headers=h)
    return resp.json()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
