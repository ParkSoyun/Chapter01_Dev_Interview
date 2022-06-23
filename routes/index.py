import os

import jwt
from bson import ObjectId
from dotenv import load_dotenv
from flask import render_template, Blueprint, jsonify, request

from datetime import datetime
from database import MongoDB

# load env SECRET_KEY
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

# Connect DB
db = MongoDB().db

index = Blueprint('index', __name__)


def make_unsolved_list(user_email):
    solved_set = set(db.user.find({'email': user_email}, {'_id': False, 'solved': True})[0]['solved'])
    total_question = db.question.estimated_document_count()
    total_question_set = set(list(range(1, total_question + 1)))

    unsolved_list = list(total_question_set.difference(solved_set))

    return unsolved_list


@index.route('/question', methods=["GET"])
def show_question():
    token_receive = request.cookies.get('mytoken')

    if token_receive is None:
        question_info = db.question.find_one({'num': 1}, {'_id': False})
        total_question = db.question.estimated_document_count()

        min_qn = 1
        max_qn = total_question

        # return jsonify({'question_info': question_info, 'min_qn': min_qn, 'max_qn': max_qn})
        return render_template("index.html", question_info=question_info, min_qn=min_qn, max_qn=max_qn)
    else:
        signin_status = True
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_email = payload['id']

        user_info = db.user.find_one({'email': user_email})

        unsolved_list = make_unsolved_list(user_email)
        sorted_unsolved = sorted(unsolved_list)

        min_qn = min(sorted_unsolved)
        max_qn = max(sorted_unsolved)

        question_info = db.question.find_one({'num': min_qn}, {'_id': False})

        # return jsonify({'question_info': question_info, 'min_qn': min_qn, 'max_qn': max_qn})
        return render_template("index.html", signIn=signin_status, user_info=user_info, question_info=question_info, min_qn=min_qn, max_qn=max_qn)


@index.route('/prevquestion', methods=["GET"])
def prev_question():
    token_receive = request.cookies.get('mytoken')

    current_qn = int(request.args.get('current_qn'))

    if token_receive is None:
        question_info = db.question.find_one({'num': current_qn-1}, {'_id': False})
        total_question = db.question.estimated_document_count()

        min_qn = 1
        max_qn = total_question

        # return render_template("index.html", question_info=question_info, min_qn=min_qn, max_qn=max_qn)
        return jsonify({'question_info': question_info, 'min_qn': min_qn, 'max_qn': max_qn})
    else:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_email = payload['id']

        unsolved_list = make_unsolved_list(user_email)
        reversed_unsolved = unsolved_list[::-1]

        min_qn = min(reversed_unsolved)
        max_qn = max(reversed_unsolved)

        for unsolved in reversed_unsolved:
            if unsolved < current_qn:
                next_qn = unsolved

                question_info = db.question.find_one({'num': next_qn}, {'_id': False})

                return jsonify({'question_info': question_info, 'min_qn': min_qn, 'max_qn': max_qn})


@index.route('/nextquestion', methods=["GET"])
def next_question():
    token_receive = request.cookies.get('mytoken')

    current_qn = int(request.args.get('current_qn'))

    if token_receive is None:
        question_info = db.question.find_one({'num': current_qn + 1}, {'_id': False})
        total_question = db.question.estimated_document_count()

        min_qn = 1
        max_qn = total_question

        return jsonify({'question_info': question_info, 'min_qn': min_qn, 'max_qn': max_qn})
        # return render_template("index.html", question_info=question_info, min_qn=min_qn, max_qn=max_qn)
    else:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_email = payload['id']

        unsolved_list = make_unsolved_list(user_email)
        sorted_unsolved = sorted(unsolved_list)

        min_qn = min(sorted_unsolved)
        max_qn = max(sorted_unsolved)

        for unsolved in sorted_unsolved:
            if unsolved > current_qn:
                next_qn = unsolved

                question_info = db.question.find_one({'num': next_qn}, {'_id': False})

                return jsonify({'question_info': question_info, 'min_qn': min_qn, 'max_qn': max_qn})


@index.route('/answer', methods=["POST"])
def save_answer():
    token_receive = request.cookies.get('mytoken')

    if token_receive is None:
        return save_answer_without_login()
    else:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_email = payload['id']

        return save_answer_with_login(user_email)


def save_answer_without_login():
    return jsonify({'msg': '로그인 후 등록이 가능합니다.'})


def save_answer_with_login(user_email):
    question_num = int(request.form['question_num'])
    answer = request.form['answer']

    now = datetime.now()
    created_at = now.strftime('%Y-%m-%d %H:%M:%S')

    answer = {
        'created_at': created_at,
        'question_num': int(question_num),
        'user_email': user_email,
        'answer': answer,
        'like_count': 0,
        'like': []
    }

    if db.answer.insert_one(answer):
        db.user.update_one({'email': 'test@test.test'}, {'$push': {'solved': int(question_num)}})

        question_info = db.question.find_one({'num': question_num}, {'_id': False})

        # temp_answer_list= list(db.answer.find({'question_num': question_num}, {'_id': False}).sort('like_count', -1))
        temp_answer_list= list(db.answer.find({'question_num': question_num}).sort('like_count', -1))

        for temp_answer in temp_answer_list:
            temp_answer['_id'] = str(temp_answer['_id'])

        answer_list = list()

        for answer in temp_answer_list:
            if answer['user_email'] == user_email:
                answer_list.append(answer)
                temp_answer_list.remove(answer)
                break

        for answer in temp_answer_list:
            answer_list.append(answer)

        unsolved_list = make_unsolved_list(user_email)

        min_qn = min(unsolved_list)
        max_qn = max(unsolved_list)

        return jsonify({'msg': '답변 등록이 완료되었습니다.', 'question_info': question_info, 'answer_list': answer_list, 'min_qn': min_qn, 'max_qn': max_qn})
    else:
        return jsonify({'msg': '답변 등록에 실패하였습니다.'})


@index.route('/answer', methods=["GET"])
def sort_answer():
    flag = int(request.args.get('flag'))
    question_num = int(request.args.get('question_num'))

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_email = payload['id']

    if flag == 1:
        question_info = db.question.find_one({'num': question_num}, {'_id': False})

        temp_answer_list = list(db.answer.find({'question_num': question_num}).sort('like_count', -1))

        for temp_answer in temp_answer_list:
            temp_answer['_id'] = str(temp_answer['_id'])

        answer_list = list()

        for answer in temp_answer_list:
            if answer['user_email'] == user_email:
                answer_list.append(answer)
                temp_answer_list.remove(answer)
                break

        for answer in temp_answer_list:
            answer_list.append(answer)

        return jsonify({'question_info': question_info, 'answer_list': answer_list})
    elif flag == 2:
        question_info = db.question.find_one({'num': question_num}, {'_id': False})

        temp_answer_list = list(db.answer.find({'question_num': question_num}).sort('created_at', -1))


        for temp_answer in temp_answer_list:
            temp_answer['_id'] = str(temp_answer['_id'])

        # answer_list = list()
        #
        # for answer in temp_answer_list:
        #     if answer['user_email'] == user_email:
        #         answer_list.append(answer)
        #         temp_answer_list.remove(answer)
        #         break
        #
        # for answer in temp_answer_list:
        #     answer_list.append(answer)

        return jsonify({'question_info': question_info, 'answer_list': temp_answer_list})


@index.route('/answer', methods=["PUT"])
def edit_answer():
    flag = int(request.form['flag'])

    if flag == 0:
        answer_comment = request.form['answer_comment']

        return jsonify({'msg': '답변을 수정합니다.', 'answer_comment': answer_comment})
    elif flag == 1:
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_email = payload['id']

        question_num = int(request.form['question_num'])
        new_answer = request.form['new_answer']

        db.answer.update_one({'user_email': user_email, 'question_num': question_num}, {'$set': {'answer': new_answer}})

        answer_info = db.answer.find_one({'user_email': user_email, 'question_num': question_num}, {'_id': False})

        return jsonify({'answer_info': answer_info})


@index.route('/answerlike', methods=["POST"])
def like_answer():
    flag = int(request.form['flag'])
    answer_id = request.form['answer_id']

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_email = payload['id']

    if flag == 0:
        db.answer.update_one({'_id': ObjectId(answer_id)}, {'$inc': {'like_count': 1}, '$push': {'like': user_email}})

        answer_info = db.answer.find_one({'_id': ObjectId(answer_id)}, {'_id': False})

        return jsonify({'answer_id': answer_id, 'answer_info': answer_info})
    elif flag == 1:
        db.answer.update_one({'_id': ObjectId(answer_id)}, {'$inc': {'like_count': -1}, '$pull': {'like': user_email}})

        answer_info = db.answer.find_one({'_id': ObjectId(answer_id)}, {'_id': False})

        return jsonify({'answer_id': answer_id, 'answer_info': answer_info})
