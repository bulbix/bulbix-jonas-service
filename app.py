import json
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



@app.route('/redmine', methods=['POST'])
def redmine():
    content = request.json
    action = content['payload']['action']
    subject = content['payload']['issue']['subject']
    taskjira = content['payload']['issue']['custom_field_values'][0]['value']
    status = content['payload']['issue']['status']['name']
    payload = {"action": action, "subject": subject, "taskJira": taskjira, "status": status}
    text = json.dumps(payload)
    response = {"text": text}
    headers = {'content-type': 'application/json'}
    requests.post(
        'https://chat.googleapis.com/v1/spaces/AAAAzd2ccJM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token'
        '=Aldpc7cSEUg59siIDFg1rtssF_-J3N-VvA7KoyBooDM%3D',
        headers=headers, data=json.dumps(response))
    return response


@app.route('/gogs', methods=['POST'])
def gogs():
    content = request.json
    repository = content['repository']['name']
    committer = content['commits'][0]['committer']["name"]
    message = content['commits'][0]['message']
    payload = {"repository": repository, "committer": committer, "message": message}
    text = json.dumps(payload)
    response = {"text": text}
    headers = {'content-type': 'application/json'}
    requests.post(
        'https://chat.googleapis.com/v1/spaces/AAAAzd2ccJM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token'
        '=fPb0sq3hVIiz6_QgotRukr8L6AD4BUXOEmCbcUMt2Qg%3D',
        headers=headers, data=json.dumps(response))
    return response


if __name__ == '__main__':
    app.run()
