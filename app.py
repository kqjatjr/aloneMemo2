from flask import Flask, request
from flask.json import jsonify
from flask.templating import render_template
from pymongo import MongoClient
from flask.json import JSONEncoder
from bson import ObjectId


# ObjectId 부분을 기본 문자열로 바꿔 줍니다
class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super().default(o)


app = Flask(__name__)
app.json_encoder = MongoJSONEncoder


client = MongoClient('localhost', 27017)
db = client.myMemo


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/myMemo', methods=['POST'])
def postMemo():
    title = request.json['title']
    memo = request.json['memo']
    db.myMemo.insert_one({'title': title, 'memo': memo})
    return jsonify({'success': True})


@app.route('/api/myMemo/list', methods=['GET'])
def getMemoList():
    memos = list(db.myMemo.find({}))
    return jsonify({'memos': memos})


@app.route('/api/myMemo/<id>', methods=['DELETE'])
def deleteMemo(id):
    db.myMemo.delete_one({'_id': ObjectId(id)})
    return jsonify({'success': True})


@app.route('/api/myMemo/<id>', methods=['GET'])
def getMemo(id):
    memo = db.myMemo.find_one({'_id': ObjectId(id)})
    return jsonify({'memo': memo})


@app.route('/api/myMemo/<id>', methods=["PUT"])
def putMemo(id):
    title = request.json['title']
    memo = request.json['memo']
    db.myMemo.update_one({'_id': ObjectId(id)}, {
        '$set': {'title': title, 'memo': memo}})
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
