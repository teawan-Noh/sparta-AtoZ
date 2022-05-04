from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient


app = Flask(__name__)

# client = MongoClient('13.209.18.100', 27017, username="test", password="test")
client = MongoClient("mongodb://localhost:27017/")
db = client.dbsparta_plus_week3


@app.route('/')
def main():
    return render_template("index.html")

@app.route('/matjip', methods=["GET"])
def get_matjip():
    # 맛집 목록을 반환하는 API
    matjip_list = list(db.matjips.find({}, {'_id': False}))
    # matjip_list 라는 키 값에 맛집 목록을 담아 클라이언트에게 반환합니다.
    # print(matjip_list)
    return jsonify({'result': 'success', 'matjip_list': matjip_list})

@app.route('/like_matjip', methods=["POST"])
def like_matjip():
    title = request.form['title_give']
    address = request.form['address_give']
    action = request.form['action_give']
    print(title, action)

    if action == 'unlike':
        db.matjips.update_one({'title': title, 'address': address}, {'$unset': {'like': False}})
    else:
        db.matjips.update_one({'title': title, 'address': address}, {'$set': {'like': True}})

    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)