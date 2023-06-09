import sqlite3
import os
from flask import Flask, render_template, request, url_for, flash, redirect, send_from_directory, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_session import Session
from flask_session_captcha import FlaskSessionCaptcha
from werkzeug.exceptions import abort
from cachelib import FileSystemCache
from forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bPYE7F9T<yJe48rC+3$TWATm=A9gm26c'
app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 5
app.config['CAPTCHA_WIDTH'] = 200
app.config['CAPTCHA_HEIGHT'] = 38
app.config['SESSION_TYPE'] = 'filesystem'

# Enables server session
Session(app)
# Initialize FlaskSessionCaptcha
captcha = FlaskSessionCaptcha(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Zaloguj się, aby korzystać z tej strony."
login_manager.login_message_category = "danger"

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.authenticated = False

        def is_active(self):
            return self.is_active()

        def is_anonymous(self):
            return False

        def is_authenticated(self):
            return self.authenticated

        def is_active(self):
            return True

        def get_id(self):
            return self.id

@login_manager.user_loader
def load_user(user_id):
   conn = get_db_connection()
   curs = conn.cursor()
   curs.execute("SELECT * from login where id = (?)",[user_id])
   lu = curs.fetchone()
   if lu is None:
      return None
   else:
      return User(int(lu[0]), lu[1], lu[2])

@app.route("/login", methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
     return redirect(url_for('profile'))
  form = LoginForm()
  if form.validate_on_submit():
     conn = get_db_connection()
     curs = conn.cursor()
     curs.execute("SELECT * FROM login where username = (?)",    [form.username.data])
     user = list(curs.fetchone())
     Us = load_user(user[0])
     if form.username.data == Us.username and form.password.data == Us.password:
        login_user(Us, remember=form.remember.data)
        flash('Zalogowano poprawnie.', 'success')
        return redirect(url_for('index'))
     else:
        flash('Zły login lub hasło', 'warning')
  return render_template('login.html',title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/')
def index():
    sort_on = request.args.get('sort_on', None)

    if (sort_on == 'cool'):
        args = 'vote desc'
    elif (sort_on == 'notcool'):
        args = 'vote asc'
    elif (sort_on == 'datasc'):
        args = 'created asc'
    elif (sort_on == 'datdesc'):
        args = 'created desc'
    else:
        args = 'id desc'

    conn = get_db_connection()
    query = 'SELECT * FROM posts ORDER BY {args}'.format(args=args)
    posts = conn.execute(query).fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        content = request.form['content']

        if not content:
            flash('Wpis jest wymagany!', 'info')
        elif(not captcha.validate()):
            flash('Przepisz poprawnie kod z obrazka!', 'info')
        else:
            conn = get_db_connection()

            content_insert = "INSERT INTO posts (content) VALUES (?);"
            data_tuple = (content,)
            conn.execute(content_insert, data_tuple)

            conn.commit()
            conn.close()
            flash('Dodano nowy wpis.', 'info')
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        content = request.form['content']

        if not content:
            flash('Treść jest wymagana!', 'info')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET content = ?, created = CURRENT_TIMESTAMP'
                         ' WHERE id = ?',
                         (content, id))
            conn.commit()
            conn.close()
            flash('Edytowano pomyślnie!', 'info')
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{:32}" został pomyślnie usunięty!'.format(post['content']),'success')
    return redirect(url_for('index'))

@app.route('/<int:id>/resetcool', methods=('GET', 'POST'))
@login_required
def resetcool(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('UPDATE posts SET vote=0 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Zresetowano poziom fajności!', 'info')
    return redirect(url_for('index'))

@app.route('/<int:id>/cool', methods=('GET', 'POST'))
def cool(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('UPDATE posts SET vote=vote+1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Ustawiono poziom fajności 👍 !', 'light')
    return redirect(url_for('index'))


@app.route('/<int:id>/notcool', methods=('GET', 'POST'))
def notcool(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('UPDATE posts SET vote=vote-1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Ustawiono poziom fajności 👎 !', 'light')
    return redirect(url_for('index'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()