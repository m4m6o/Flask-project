# -*- coding: utf-8 -*-
from flask import Flask, url_for, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from loginform import LoginForm 
from addnewsform import AddNewsForm
from regform import RegForm
from commentform import CommentForm
from usersmodel import UsersModel
from newsmodel import NewsModel
from commentsmodel import CommentsModel
from editform import EditForm
from shutil import copy
from db import DB
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
users_db = DB('users.db')
news_db = DB('news.db')
comments_db = DB('comments.db')
users_init = UsersModel(users_db.get_connection())
users_init.init_table()
news_init = NewsModel(news_db.get_connection())
news_init.init_table()
comments_init = CommentsModel(comments_db.get_connection())
comments_init.init_table()

@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    news = NewsModel(news_db.get_connection()).get_all()
    news.sort(key=lambda x: x[3])
    news.reverse()
    user_model = UsersModel(users_db.get_connection())    
    usernames = {}
    for item in news:
        data = user_model.get(item[4])
        if item[4] not in usernames:
            usernames.update({item[4]: [str(data[2] + ' ' + data[3]), data[1]]})

    return render_template('index.html', title='Messages', username=session['username'],  cur_user_id=session['user_id'],
                           news=news, users=usernames)

@app.route('/<int:user_id>')
def user_data(user_id):
    if 'username' not in session:
        return redirect('/login')    
    user_model = UsersModel(users_db.get_connection())
    data = user_model.get(user_id)
    news = NewsModel(news_db.get_connection()).get_all(user_id)
    path = data[6]
    if session['user_id'] == user_id:
        my_page = True
    else:
        my_page = False
    name_surname = data[2] + ' ' + data[3]
    return render_template('user_data.html', title=name_surname, my_page=my_page, cur_user_id=session['user_id'], path=path, name=data[2], surname=data[3], status=data[4],
                           news=news)    

@app.route('/edit', methods=['GET', 'POST'])
def user_edit():
    if 'username' not in session:
        return redirect('/login')
    form = EditForm()
    if form.validate_on_submit():
        url = form.photo.data
        status = form.status.data
        nm = UsersModel(users_db.get_connection())
        nm.update_status(status, session['user_id'])
        nm.update_photo(url, session['user_id'])
        my_page = '/' + str(session['user_id'])
        return redirect(my_page)
    return render_template('edit.html', title='Edit', form=form, my_page=False, cur_user_id=session['user_id'], username=session['username'])  

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    if form.validate_on_submit():
        username = form.username.data
        name = form.name.data
        surname = form.surname.data
        password = form.password.data
        confirm = form.confirm.data
        password_hash = generate_password_hash(password)
        user_model = UsersModel(users_db.get_connection())
        exists = user_model.exists(username, password_hash)
        if not exists[0] and password == confirm:            
            user_model.insert(username, name, surname, password_hash)
            exists = user_model.exists(username, password_hash)
            session['username'] = username
            session['user_id'] = exists[1]         
            return redirect("/index")
    return render_template('reg.html', title='Sign up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(users_db.get_connection())
        true_pass = user_model.password_check(user_name)
        exists = user_model.exists(user_name, true_pass)
        if check_password_hash(true_pass, password) and exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
            return redirect("/index")
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')

@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:
        return redirect('/login')
    form = AddNewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        date = datetime.datetime.now()
        nm = NewsModel(news_db.get_connection())
        nm.insert(title, content, str(date.day) + '.' + str(date.month) + '.' + str(date.year), session['user_id'])
        return redirect("/index")
    return render_template('add_news.html', title='Добавить новость',  cur_user_id=session['user_id'],
                           form=form, username=session['username'])
 
@app.route('/news/<int:news_id>', methods=['GET', 'POST'])
def news_data(news_id):
    if 'username' not in session:
        return redirect('/login')
    form = CommentForm()
    if form.validate_on_submit():
        content = form.content.data
        cm = CommentsModel(comments_db.get_connection())
        author_data = UsersModel(users_db.get_connection()).get(session['user_id'])
        username = author_data[2] + ' ' + author_data[3]        
        cm.insert(session['user_id'], news_id, content, username)
        return redirect("/news/" + str(news_id))
    news = NewsModel(news_db.get_connection()).get(news_id)
    author_data = UsersModel(users_db.get_connection()).get(news[4])
    username = author_data[2] + ' ' + author_data[3]
    cm = CommentsModel(comments_db.get_connection()).get_all(news[0])
    cm.reverse()
    return render_template('news_data.html', title=news[1], author=username,  cur_user_id=session['user_id'],
                           news=news, cm=cm, form=form)
 
@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(news_db.get_connection())
    nm.delete(news_id)
    cm = CommentsModel(comments_db.get_connection())
    cm.news_delete(news_id)
    return redirect("/index")

@app.route('/delete_comment/<int:comment_id>', methods=['GET'])
def delete_comment(comment_id):
    if 'username' not in session:
        return redirect('/login')
    cm = CommentsModel(comments_db.get_connection())
    cm.delete(comment_id)
    return redirect("/index")

@app.route('/admin_only')
def admin_only():
    if 'username' not in session:
        return redirect('/login')
    news = NewsModel(news_db.get_connection()).get_all()
    news.sort(key=lambda x: x[3])
    return render_template('index.html', username=session['username'],
                           news=news)

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')