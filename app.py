from flask import Flask , session, render_template , redirect , request
from werkzeug.datastructures import Authorization
from data import Articles
from passlib.hash import sha256_crypt
from functools import wraps
import pymysql

db = pymysql.connect(
    host='localhost', 
    user='root', 
    password='1234', 
    db='gangnam', 
    charset='utf8mb4')

cur = db.cursor()

app = Flask(__name__)
app.debug = True

def is_logged_in(f):
    @wraps(f)
    def _wraps(*args, **kwargs):
        if 'is_logged' in session:
            # query = f"SELECT username FROM users WHERE email = '{session['username']}'"
            # cur.execute(query)
            # db.commit()
            # user = cur.fetchone()
            # # print(user)
            # user_name = user[0]
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return _wraps

def is_admin(f):
    @wraps(f)
    def _wraps(*args, **kwargs):
        if session['email'] == '1@naver.com':
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return _wraps

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password = sha256_crypt.encrypt(password)
        # print(password_1)
        # print(sha256_crypt.verify("1234", password_1))
        sql = f"SELECT email FROM users WHERE email = '{email}'"

        cur.execute(sql)

        db.commit()

        user_email = cur.fetchone()
        if user_email == None:
            query = f"INSERT INTO users (name, email, username, password) VALUES('{name}','{email}','{username}','{password}')"
            
            cur.execute(query)

            db.commit()
            return redirect('/login')
        else:
            return redirect('/register')
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        query = f"SELECT * FROM users WHERE email = '{email}'"
        cur.execute(query)
        db.commit()
        user = cur.fetchone()
        # print(user)
        
        if user == None:
            return redirect('/login')
        else:
            if sha256_crypt.verify(password, user[4]):
                session['is_logged'] = True
                session['email'] = user[2]
                session['username'] = user[3]
                # print(session)
                return redirect('/')
            else:
                return redirect ('/login')

    else:
        return render_template('login.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('login')


@app.route('/', methods=['GET','POST'])
def hello_world():
    return render_template('home.html', user_name = session['username'])


@app.route('/about',methods=['GET','POST'])
@is_logged_in
def about():
    return render_template('about.html', user_name = session['username'])


@app.route('/articles',methods=['GET','POST'])
@is_logged_in
def articles():
    # articles = Articles()
    query = 'SELECT * FROM topic'

    cur.execute(query)

    db.commit()

    articles = cur.fetchall()

    # print(articles)
    return render_template('articles.html', articles = articles, user_name = session['username'])


@app.route('/article/<id>',methods=['GET','POST'])
@is_logged_in
def article(id):
    # # articles = Articles()
    # print(len(articles))
    # if len(articles)>=int(id):
    #     article = articles[int(id)-1]
    #     return render_template('article.html', article = article)
    # else:
    #     return render_template('article.html', article = 'No Data')

    query = f'SELECT * FROM topic WHERE id = {id}'

    cur.execute(query)

    db.commit()

    article = cur.fetchone()

    print(article)

    if article == None:
        return redirect('/articles')
    else:
        return render_template('article.html', article = article, user_name = session['username'])


@app.route('/article/<id>/delete')
@is_logged_in
def delete_article(id):
    query = f'DELETE FROM `gangnam`.`topic` WHERE id = {id}'
    cur.execute(query)

    db.commit()

    return redirect('/articles')


@app.route('/add_article', methods=['GET','POST'])
@is_logged_in
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        author = request.form['author']

        query = "INSERT INTO `topic` (`title`, `description`, `author`) VALUES (%s, %s, %s)"
        input_data = [title, description, author]

        cur.execute(query, input_data)
        db.commit()
        print(cur.rowcount)
        return redirect('/articles')

    else:
        return render_template('add_article.html', user_name = session['username'])

@app.route('/article/<id>/edit', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        author = request.form['author']
        # print(title, description, author)
        # return "SUCCESS"

        query = f"UPDATE topic SET title = '{title}', description = '{description}', author = '{author}' WHERE id = {id}"
        cur.execute(query)
        db.commit()
        
        return redirect('/articles')

    else:
        query = f'SELECT * FROM topic WHERE id = {id}'
        cur.execute(query)
        db.commit()

        article = cur.fetchone()

        return render_template('edit_article.html', article = article, user_name = session['username'])


@app.route('/admin', methods = ['GET','POST'])
@is_logged_in
@is_admin
def admin():
    query = 'SELECT * FROM users'
    cur.execute(query)
    db.commit()
    user_lists = cur.fetchall()
   
    return render_template('admin.html', user_lists = user_lists, user_name = session['username'])


@app.route('/admin/<id>/edit', methods = ['GET','POST'])
@is_logged_in
@is_admin
def edit_admin(id):
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        # print(email, username)
        query = f"UPDATE users SET name = '{name}', username = '{username}' WHERE id = {id}"
        cur.execute(query)
        db.commit()

        return redirect('/admin')
    else:
        query = f'SELECT * FROM users WHERE id = {id}'
        cur.execute(query)
        db.commit()

        user_list = cur.fetchone()

        return render_template('edit_admin.html', user_list = user_list, user_name = session['username'])


@app.route('/admin/<id>/delete')
@is_logged_in
@is_admin
def delete_admin(id):
    query = f'DELETE FROM users WHERE id = {id}'
    cur.execute(query)

    db.commit()

    return redirect('/admin')

if __name__ == '__main__':
    app.secret_key = "gangnamStyle"
    app.run()