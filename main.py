from flask import Flask, url_for, redirect, render_template
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users import User
from forms.login import LoginForm
from data.news import News



app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return "Миссия Колонизация Марса"


@app.route('/index')
def deviz():
    return "И на Марсе будут яблони цвести!"


@app.route('/promotion')
def promo():
    return f'''Человечество вырастает из детства.
           <br>Человечеству мала одна планета.
           <br>Мы сделаем обитаемыми безжизненные пока планеты.
           <br>И начнем с Марса!
           <br>Присоединяйся!'''


@app.route('/promotion_image')
def promote():
    return f'''<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet" 
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                    crossorigin="anonymous">

                        <title>Привет, Марс!</title>
                      </head>
                      <body>
                      <link rel="stylesheet" 
                    <div class="alert alert-primary" role="alert">
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                        <h1>Жди нас, Марс!</h1>
                        </div>
                    <div class="alert alert-secondary" role="alert">Человечество вырастает из детства.</div>
           <div class="alert alert-success" role="alert"><br>Человечеству мала одна планета.</div>
           <div class="alert alert-secondary" role="alert"><br>Мы сделаем обитаемыми безжизненные пока планеты.</div>
           <div class="alert alert-warning" role="alert"><br>И начнем с Марса!</div>
           <div class="alert alert-danger" role="alert"><br>Присоединяйся!</div>
                        <img src="{url_for('static', filename='image/mars.jpg')}" 
               alt="здесь должна была быть картинка, но не нашлась">
                      </body>
                    </html>'''


@app.route('/image_mars')
def mars():
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">

                    <title>Привет, Марс!</title>
                  </head>
                  <body>
                    <h1>Жди нас, Марс!</h1>
                    <img src="{url_for('static', filename='image/mars.jpg')}" 
           alt="здесь должна была быть картинка, но не нашлась">
                  </body>
                </html>'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        user.set_password(form.password.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')

user = User()
user.name = "Пользователь 1"
user.about = "биография пользователя 1"
user.email = "email@email.ru"
db_sess = db_session.create_session()
db_sess.add(user)
db_sess.commit()