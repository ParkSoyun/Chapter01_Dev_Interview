from flask import Flask, render_template, request

from routes.index import index
from database import MongoDB

app = Flask(__name__)

app.register_blueprint(index)

@app.route('/')
def home():
    question_info = MongoDB().db.question.find_one({}, {'_id': False})

    return render_template("index.html", question_info=question_info)
    # return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

