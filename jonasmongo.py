import json
import re
import uuid
from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient
from models import JonasBook
import os


class JonasMongo:
    def __init__(self):
        mongodb_client = MongoClient(os.environ.get('JONAS_MONGO'))
        self.db = mongodb_client.db

    def upsert_book(self, book_request: JonasBook):
        shelf = self.db.shelf.find_one({"number": book_request.number}, {})
        print(shelf)
        request = book_request.dict()
        book = {x: request[x] for x in request}
        del book["number"]
        book['uuid'] = str(uuid.uuid4())
        book['dateCreated'] = datetime.now()
        if shelf is None:
            self.db.shelf.insert_one({'number': book_request.number, 'books': [book]})
        else:
            self.db.shelf.update_one({"number": book_request.number}, {"$push": {'books': book}})

    def search_book(self, q):
        if len(q) == 0:
            return []
        rgx = re.compile(f'.*{q}.*', re.IGNORECASE)
        books = self.db.shelf.aggregate(
            [{"$unwind": "$books"}, {"$match": {"$or": [{"books.title": rgx}, {"books.author": rgx}]}},
             {'$project': {'id': '$books.uuid', 'number': '$number', "title": "$books.title",
                           "author": "$books.author", "level": "$books.level", "section": "$books.section"}}])
        books = JSONEncoder().encode(list(books))
        return json.loads(books)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        return json.JSONEncoder.default(self, o)
