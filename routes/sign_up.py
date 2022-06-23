from flask import Blueprint
from database import MongoDB
import hashlib
from flask import render_template, jsonify, request, redirect, url_for
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os
import jwt


# load env SECRET_KEY
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

# Connect DB
db = MongoDB().db

sign_up = Blueprint('sign_up', __name__)


@sign_up.route('/signup', methods=['GET'])
def sign_up_get():
    token_receive = request.cookies.get('mytoken')
    if token_receive is None:
        return render_template('sign-up.html')
    else:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        signin_status = True
        user_info = db.user.find_one({"email": payload["id"]})
        return render_template('sign-up.html', signin_status=signin_status, user_info=user_info)


@sign_up.route('/signup', methods=['POST'])
def sign_up_post():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    email_receive = request.form['email_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "email": email_receive,
        "name": username_receive,
        "password": password_hash,
        "solved": [],
    }
    db.user.insert_one(doc)
    return jsonify({'result': 'success'})
