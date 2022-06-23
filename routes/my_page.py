from flask import Blueprint
from flask import render_template, request, jsonify, redirect, url_for
from database import MongoDB
import jwt
from dotenv import load_dotenv
import os
import hashlib

# Connect DB
db = MongoDB().db

# load env SECRET_KEY
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')


my_page = Blueprint('my_page', __name__)


@my_page.route("/checkuserinfo", methods=["GET"])
def check_user_info_get():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        signin_status = True
        user = db.user.find_one({"email": payload["id"]})
        return render_template('check-user.html', signin_status=signin_status, user_info=user)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template("sign-in.html")


@my_page.route("/checkuserinfo", methods=["POST"])
def check_user_info_post():
    password_receive = request.form['password_give']
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    user = db.user.find_one({'password': pw_hash})
    if user:
        return jsonify({'msg': 'success'})
    else:
        return jsonify({'msg': 'fail'})


@my_page.route("/userinfo", methods=["GET"])
def user_info_page():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        signin_status = True
        user = db.user.find_one({"email": payload["id"]})
        return render_template('my-page.html',signin_status=signin_status, user_info=user)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        # print(url_for('signin')) url_for에서 "werkzeug.routing.BuildError"에러남. 아마 blueprint떄문이지않을까..?
        return render_template("sign-in.html")  # render_template로 해주니 에러는 나지 않지만 chrome url에 값이 변경되지 않음.


@my_page.route("/userinfo", methods=["PUT"])
def user_info():
    name_receive = request.form['name_give']
    email_receive = request.form['email_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    db.user.update_one({'email': email_receive}, {'$set': {'name': name_receive, 'password': password_hash}})
    return jsonify({'msg': 'success'})


