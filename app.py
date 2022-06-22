from flask import Flask, render_template
from routes.sign_up import sign_up
from routes.sign_in import sign_in
from routes.my_page import my_page
from routes.index import index
from database import MongoDB

# Connect DB
db = MongoDB().db

app = Flask(__name__)

# route 등록
app.register_blueprint(my_page)
app.register_blueprint(sign_up)
app.register_blueprint(sign_in)
app.register_blueprint(index)


@app.route('/')
def home():
    question_info = db.question.find_one({'num': 1}, {'_id': False})
    total_question = db.question.estimated_document_count()

    min_qn = 1
    max_qn = total_question

    return render_template("index.html", question_info=question_info, min_qn=min_qn, max_qn=max_qn)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

