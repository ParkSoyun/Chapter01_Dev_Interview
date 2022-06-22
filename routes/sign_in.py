from flask import Blueprint
from database import MongoDB
import jwt
import datetime
import hashlib
from flask import render_template, jsonify, request, redirect, url_for
from dotenv import load_dotenv
import os
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
        payload = {
            'id': email_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})