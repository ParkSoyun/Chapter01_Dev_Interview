from flask import Blueprint
from database import MongoDB
import jwt
import datetime
import hashlib
from flask import render_template, jsonify, request, redirect, url_for
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


# load env SECRET_KEY
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

# Connect DB
db = MongoDB().db

sign_in = Blueprint('sign_in', __name__)


@sign_in.route('/signin', methods=['GET'])
def sign_in_get():
    return render_template('sign-in.html')


@sign_in.route('/signin', methods=['POST'])
def sign_in_post():
    # 로그인
    email_receive = request.form['email_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'email': email_receive, 'password': pw_hash})

    if result is not None:
        print(result)
        payload = {
            'id': email_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})



# @sign_up.route('/')
# def home():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         print(payload)
#         user_info = db.users.find_one({"username": payload["id"]})
#         return render_template('index.html', user_info=user_info)
#     except jwt.ExpiredSignatureError:
#         return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
#     except jwt.exceptions.DecodeError:
#         return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# @app.route('/user/<username>')
# def user(username):
#     # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False
#
#         user_info = db.users.find_one({"username": username}, {"_id": False})
#         return render_template('user.html', user_info=user_info, status=status)
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))




# @app.route('/sign_up/check_dup', methods=['POST'])
# def check_dup():
#     username_receive = request.form['username_give']
#     exists = bool(db.users.find_one({"username": username_receive}))
#     # print(value_receive, type_receive, exists)
#     return jsonify({'result': 'success', 'exists': exists})