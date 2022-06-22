from flask import Blueprint
from flask import Flask, render_template, request, jsonify
from database import MongoDB

# Connect DB
db = MongoDB().db

my_page = Blueprint('my_page', __name__)


@my_page.route("/check-userinfo", methods=["GET"])
def check_user_info_get():
    return render_template('check-user.html',signIn = True)


@my_page.route("/check-userinfo", methods=["POST"])
def check_user_info_post():
    password_receive = request.form['password_give']
    user = list(db.user.find({'password' : password_receive}, {'_id': False}))
    if len(user) == 1:
        return jsonify({'msg': 'success', 'user': user})
    else:
        return jsonify({'msg': 'fail'})


@my_page.route("/userinfo", methods=["GET"])
def user_info_page():
    user_receive = request.form.get('user_give', False)
    print(user_receive)
    return render_template('my-page.html', user = user_receive, signIn = True)


@my_page.route("/userinfo", methods=["POST"])
def user_info():
    name_receive = request.form['name_give']
    email_receive = request.form['email_give']
    print(name_receive, email_receive)
    return render_template('my-page.html', signIn = True)


