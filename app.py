from jonasmongo import JonasMongo
from fastapi import FastAPI, Query, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import JonasBook, User, UserInDB
from typing import Optional
import requests
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os

jonasmongo = JonasMongo()
app = FastAPI()

# START CORS
origins = [
    "http://localhost:3000",
    "https://bulbix-jonas-web.herokuapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# END CORS

# START SECURITY
fake_users_db = {
    "bulbix": {
        "username": "bulbix",
        "full_name": "Fernando Prado",
        "email": "lfpradof@gmail.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }
}


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.put("/add_book")
def add_book(current_user: User = Depends(get_current_active_user), book: JonasBook = Body(...)):
    print(current_user)
    jonasmongo.upsert_book(book)
    return {"message": "success"}


@app.post("/update_book")
def add_book(current_user: User = Depends(get_current_active_user), book: JonasBook = Body(...)):
    print(current_user)
    jonasmongo.update_book(book)
    return {"message": "success"}


@app.get("/search_book")
def search_book(
        current_user: User = Depends(get_current_active_user),
        q: Optional[str] = Query(None, max_length=50),
        sold: Optional[bool] = Query(None)
):
    print(current_user)
    result = jonasmongo.search_book(q, sold)
    return result


@app.get("/consult_isbn")
def consult_isbn(
        current_user: User = Depends(get_current_active_user),
        isbn: Optional[str] = Query(..., min_length=1, max_length=50)
):
    print(current_user)
    h = {'Authorization': os.environ.get('JONAS_ISBNDBKEY')}
    resp = requests.get(f"https://api2.isbndb.com/book/{isbn}", headers=h)
    return resp.json()


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
