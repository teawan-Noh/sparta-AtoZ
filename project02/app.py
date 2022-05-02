from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests

app = Flask(__name__)

# client = MongoClient('3.35.156.42', 27017, username="test", password="test")
client = MongoClient("mongodb://localhost:27017/")
db = client.dbsparta_plus_week2


@app.route('/')
def main():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    words = list(db.words.find({}, {"_id": False}))

    # detail 함수에서 넘겨받은 msg
    msg = request.args.get('msg')
    return render_template("index.html", words=words, msg=msg)


@app.route('/detail/<keyword>')
def detail(keyword):
    status_receive = request.args.get('status_give')
    # API에서 단어 뜻 찾아서 결과 보내기
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}", headers={"Authorization": "Token 6e9f93179a7e270b1674c204eb8815aea11fe277"})
    # 200 코드가 아닐경우 main 함수를 실행시켜줘
    if r.status_code != 200:
        return redirect(url_for("main", msg='단어가 이상해요'))
    result = r.json()
    print(result)

    return render_template("detail.html", word=keyword, result=result, status = status_receive)


@app.route('/api/save_word', methods=['POST'])
def save_word():
    # 단어 저장하기
    word_receive = request.form['word_give']
    definition_receive = request.form['definition_give']

    doc = {
        'word': word_receive,
        'definition': definition_receive
    }
    db.words.insert_one(doc)

    return jsonify({'result': 'success', 'msg': f'단어 {word_receive} 저장!'})


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    # 단어 삭제하기
    word_receive = request.form['word_give']
    db.words.delete_one({'word':word_receive})

    return jsonify({'result': 'success', 'msg': f'단어 {word_receive} 삭제!'})


@app.route('/api/get_exs', methods=['GET'])
def get_exs():
    # 예문 가져오기
    word = request.args.get('word_give')
    examples = list(db.example.find({'word': word}, {'_id': False}))
    # print(examples)
    return jsonify({'result': 'success', 'ex':examples})

@app.route('/api/save_ex', methods=['POST'])
def save_ex():
    # 예문 저장하기
    ex_receive = request.form['ex_give']
    keyword = request.form['keyword']
    # print(keyword, ex_receive)

    doc = {'word': keyword, 'example': ex_receive}
    # db.example.insert_one(doc)


    return jsonify({'result': 'success', 'msg': f'예문 {ex_receive} 저장'})


@app.route('/api/delete_ex', methods=['POST'])
def delete_ex():
    # 예문 삭제하기
    word = request.form['word_give']
    num = request.form['number_give']
    # print(word, num)
    example = list(db.example.find({'word': word}, {'_id': False}))[int(num)]['example']
    # print(word, example)

    db.example.delete_one({'word': word, "example":example})

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)