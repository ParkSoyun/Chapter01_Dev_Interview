from flask import Flask, render_template, request
from routes.sign_up import sign_up
from routes.sign_in import sign_in
from routes.my_page import my_page
from routes.index import index
from routes.my_question import my_question
import jwt
from dotenv import load_dotenv
import os

from database import MongoDB

# load env SECRET_KEY
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

# Connect DB
db = MongoDB().db

app = Flask(__name__)

# route 등록
app.register_blueprint(my_page)
app.register_blueprint(sign_up)
app.register_blueprint(sign_in)
app.register_blueprint(index)
app.register_blueprint(my_question)


def make_unsolved_list(user_email):
    solved_set = set(db.user.find({'email': user_email}, {'_id': False, 'solved': True})[0]['solved'])
    total_question = db.question.estimated_document_count()
    total_question_set = set(list(range(1, total_question + 1)))

    unsolved_list = list(total_question_set.difference(solved_set))

    return unsolved_list


@app.route('/')
def home():
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
        return render_template("index.html", signin_status=signin_status, user_info=user_info,
                               question_info=question_info, min_qn=min_qn, max_qn=max_qn)



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

