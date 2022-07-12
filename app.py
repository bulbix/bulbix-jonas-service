from jonasmongo import JonasMongo
import requests
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
jonasmongo = JonasMongo(app)


@app.route("/add_book", methods=['POST'])
@cross_origin()
def add_book():
    content = request.json
    jonasmongo.upsert_book(content)
    return jsonify(message="success")


@app.route("/search_book", methods=['GET'])
@cross_origin()
def search_book():
    result = jonasmongo.search_book(request.args.get('title'), request.args.get('author'))
    return result


@app.route("/consult_isbn", methods=['GET'])
@cross_origin()
def consult_isbn():
    h = {'Authorization': 'xxxx'}
    resp = requests.get(f"https://api2.isbndb.com/book/{request.args.get('isbn')}", headers=h)
    return resp.json()


if __name__ == '__main__':
    app.run()
