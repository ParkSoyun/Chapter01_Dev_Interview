from flask import Flask
from routes.my_page import my_page

app = Flask(__name__)

# route 등록
app.register_blueprint(my_page)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
