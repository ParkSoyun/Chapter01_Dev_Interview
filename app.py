from flask import Flask
from routes.sign_up import sign_up
from routes.sign_in import sign_in
from routes.my_page import my_page
from routes.index import index
from routes.my_question import my_question


app = Flask(__name__)

# route 등록
app.register_blueprint(my_page)
app.register_blueprint(sign_up)
app.register_blueprint(sign_in)
app.register_blueprint(index)
app.register_blueprint(my_question)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
