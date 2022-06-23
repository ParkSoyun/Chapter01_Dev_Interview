from flask import Blueprint
from flask import render_template, request, jsonify, redirect, url_for
from database import MongoDB
import jwt
from dotenv import load_dotenv
import os

# Connect DB
db = MongoDB().db

# load env SECRET_KEY
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')


my_question = Blueprint('my_question', __name__)


@my_question.route("/myquestion", methods=["GET"])
def check_user_info_get():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        signin_status = True
        user = db.user.find_one({"email": payload["id"]})
        solved_list = user['solved']
        question_list = []
        for solved in solved_list:
            question_collection = db.question.find_one({"num": int(solved)})
            question_num = question_collection['num']
            question = question_collection['question']
            answer_collection = db.answer.find_one({"question_num": int(solved), "user_email": payload["id"]})
            if answer_collection != "None":
                answer = answer_collection['answer']
                like_count = answer_collection['like_count']
            # print(question_collection)
            # print(answer_collection)
            question_list.append((question_num, question, answer, like_count))

        return render_template('my-question.html', signin_status=signin_status, user_info=user, question_list=question_list)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template("sign-in.html")