import datetime

from flask_pymongo import PyMongo
import re
import json
from bson import ObjectId
import uuid


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        return json.JSONEncoder.default(self, o)


class JonasMongo:
    def __init__(self, app=None):
        app.config["MONGO_URI"] = "mongodb://jonas:jonas123@localhost:27017/jonas?authSource=admin"
        mongodb_client = PyMongo(app)
        self.db = mongodb_client.db

    def upsert_book(self, request):
        shelf = self.db.shelf.find_one({"number": request['number']}, {})
        print(shelf)

        book = {'uuid': str(uuid.uuid4()), 'title': request['title'], 'author': request['author'],
                'sold': request['sold'], 'level': request['level'], 'section': request['section']}
        if shelf is None:
            self.db.shelf.insert_one({'number': request['number'], 'books': [book]})
        else:
            self.db.shelf.update({"number": request['number']}, {"$push": {'books': book}})

    def search_book(self, title, author):
        rgx1 = re.compile(f'.*{title}.*', re.IGNORECASE)  # compile the regex
        rgx2 = re.compile(f'.*{author}.*', re.IGNORECASE)
        books = self.db.shelf.aggregate(
            [{"$unwind": "$books"}, {"$match": {"$and": [{"books.title": rgx1}, {"books.author": rgx2}]}},
             {'$project': {'id': '$books.uuid', 'number': '$number', "title": "$books.title",
                           "author": "$books.author","level":"$books.level", "section":"$books.section"}}])
        books = JSONEncoder().encode(list(books))
        print(books)
        return books
