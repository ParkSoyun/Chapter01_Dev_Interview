from flask import render_template, Blueprint, jsonify, request

from datetime import datetime
from database import MongoDB

index = Blueprint('index', __name__)


@index.route('/question', methods=["GET"])
def show_question():
    user_email = request.args.get('email')
    print(user_email)

    if user_email is None:
        total_question = MongoDB().db.question.estimated_document_count()

        min_qn = 1
        max_qn = total_question

        question_info = MongoDB().db.question.find_one({}, {'_id': False})

        return jsonify({'question_info': question_info, 'min_qn': min_qn, 'max_qn': max_qn})
        # return render_template("index.html", question_info=question_info)
    else:
        solved_set = set(MongoDB().db.user.find({'email': user_email}, {'_id': False, 'solved': True})[0]['solved'])
        total_question = MongoDB().db.question.estimated_document_count()
        total_question_set = set(list(range(1, total_question + 1)))

        unsolved_list = list(total_question_set.difference(solved_set))
        sorted_unsolved = sorted(unsolved_list)

        min_qn = min(sorted_unsolved)
        max_qn = max(sorted_unsolved)

        question_info = MongoDB().db.question.find_one({'num': min_qn}, {'_id': False})

        return jsonify({'question_info': question_info, 'min_qn': min_qn, 'max_qn': max_qn})


@index.route('/prevquestion', methods=["GET"])
def prev_question():
    user_email = request.args.get('email')
    current_qn = int(request.args.get('current_qn'))

    solved_set = set(MongoDB().db.user.find({'email': user_email}, {'_id': False, 'solved': True})[0]['solved'])
    total_question = MongoDB().db.question.estimated_document_count()
    total_question_set = set(list(range(1, total_question+1)))

    unsolved_list = list(total_question_set.difference(solved_set))
    reversed_unsolved = unsolved_list[::-1]

    min_qn = min(reversed_unsolved)
    max_qn = max(reversed_unsolved)

    for unsolved in reversed_unsolved:
        print(unsolved, current_qn)
        if unsolved < current_qn:
            next_qn = unsolved

            question_info = MongoDB().db.question.find_one({'num': next_qn}, {'_id': False})

            return jsonify({'question_info': question_info, 'min_qn': min_qn, 'max_qn': max_qn})


@index.route('/nextquestion', methods=["GET"])
def next_question():
    user_email = request.args.get('email')
    current_qn = int(request.args.get('current_qn'))

    solved_set = set(MongoDB().db.user.find({'email': user_email}, {'_id': False, 'solved': True})[0]['solved'])
    total_question = MongoDB().db.question.estimated_document_count()
    total_question_set = set(list(range(1, total_question+1)))

    unsolved_list = list(total_question_set.difference(solved_set))
    sorted_unsolved = sorted(unsolved_list)

    min_qn = min(sorted_unsolved)
    max_qn = max(sorted_unsolved)

    for unsolved in sorted_unsolved:
        if unsolved > current_qn:
            next_qn = unsolved

            question_info = MongoDB().db.question.find_one({'num': next_qn}, {'_id': False})

            return jsonify({'question_info': question_info, 'min_qn': min_qn, 'max_qn': max_qn})


@index.route('/answer', methods=["POST"])
def save_answer():
    user_email = request.form['email']

    if user_email == '':
        return save_answer_without_login()
    else:
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

    if MongoDB().db.answer.insert_one(answer):
        MongoDB().db.user.update_one({'email': 'test@test.test'}, {'$push': {'solved': int(question_num)}})

        question_info = MongoDB().db.question.find_one({'num': question_num}, {'_id': False})

        answer_list = list(MongoDB().db.answer.find({'question_num': question_num}, {'_id': False}))


        # temp_answer_list = MongoDB().db.answer.find({'question_num': question_num}, {'_id': False}).sort({'like_count': -1})
        #
        # my_answer = sorted(temp_answer_list, key = lambda x: 'like_count')

        return jsonify({'msg': '답변 등록이 완료되었습니다.', 'question_info': question_info, 'answer_list': answer_list})
    else:
        return jsonify({'msg': '답변 등록에 실패하였습니다.'})