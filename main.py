from flask import Flask, render_template, session, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, UserMixin, logout_user
import uuid
import re


app = Flask(__name__)
app.secret_key = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager(app)


class Users(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    login = db.Column(db.String, unique=True, nullable=False)
    psw = db.Column(db.String, nullable=False)

    def __repr__(self):
        return (f'id: {self.id}, '
                f'login:{self.login}'
                f'psw: {self.psw}')


class Tasks(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    users_id = db.Column(db.String)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.String, nullable=False)
    hardness = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean)

    def __repr__(self):
        return (f'id: {self.id}'
                f'users_id:{self.users_id}'
                f'title: {self.title}'
                f' due_date: {self.due_date}'
                f'hardness: {self.hardness}'
                f'done: {self.done}')


with app.app_context():
    db.create_all()


def get_user(Users, user_id):
    try:
        result = Users.query.filter_by(id=user_id).all()
        if not result:
            return False
        return result
    except:
        print('Error getting data from db')
    return False


class UserLogin(UserMixin):

    def FromDB(self, Users, user_id):
        self.__user = get_user(Users, user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    # def is_authenticated(self):
    #     return True
    #
    # def is_active(self):
    #     return True
    #
    # def is_anonymous(self):
    #     return False

    def get_id(self):
        return str(self.__user.id)


@login_manager.user_loader
def load_user(user_id):
    session['id'] = user_id
    print('load_user')
    print(session)
    return db.session.query(Users).get(user_id)


@app.route('/', methods=['POST', 'GET'])
def index():
    if current_user.is_authenticated:
        tasks = Tasks.query.filter_by(users_id=session['id']).all()
        return render_template('index.html', Tasks=tasks)
    return render_template('index.html')


@app.route('/add_task', methods=['POST', 'GET'])
def add_task():
    print(session)
    if request.method == 'POST':
        if current_user.is_authenticated:
            userid = session['id']
            title = request.form['title']
            selected_hardness = request.form.get('hardness')
            selected_due_date = request.form.get('duedate')
            task = Tasks(users_id=userid, title=title, due_date=selected_due_date, hardness=selected_hardness, done=False)
            try:
                db.session.add(task)
                db.session.flush()
                db.session.commit()
            except:
                db.session.rollback()
                flash('Error adding new task')
            return redirect(url_for('index'))
        flash('User not logged in')
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/done', methods=['POST'])
def done():
    if request.method == 'POST':
        done_tasks = request.form.getlist('done_checkbox')
        for id in done_tasks:
            task = Tasks.query.filter_by(id=id).first()
            try:
                db.session.delete(task)
                db.session.commit()
                flash('Tasks have been deleted successfully')
            except:
                flash('Error deleting done tasks')
        return redirect(url_for('index'))
    return redirect(url_for('index'))



@app.route('/registr', methods=['POST', 'GET'])
def registr():
    if request.method == 'POST':
        try:
            id = str(uuid.uuid4())
            login = request.form['login']
            if re.findall(r'\d', login) and re.findall(r'\D', login) and re.findall(r'\w{8,}'):
                if Users.query.filter_by(login=login).count() == 0:
                    hashed_psw = generate_password_hash(request.form['psw'])
                    user = Users(id=id, login=login, psw=hashed_psw)
                    db.session.add(user)
                    db.session.flush()
                    db.session.commit()
                    loggeduser = UserLogin().create(user)
                    login_user(loggeduser)
                    flash('You have been signed up and logged in')
                else:
                    flash('Such user already exists')
            else:
                flash('Weak password! '
                      'It must contain 0-9 and and any letter. '
                      'At least 8 symbols.')
        except:
            db.session.rollback()
            flash('Registration error')
    return redirect(url_for('index'))


@app.route('/login', methods=['POST', 'GET'])
def autho():
    if request.method == 'POST':
        user = Users.query.filter_by(login=request.form['login']).first()
        if user and check_password_hash(user.psw, request.form['psw']):
            loggeduser = UserLogin().create(user)
            session['id'] = user.id
            login_user(loggeduser)
            flash('User log in successfully')
            session['userLogged'] = True
            return redirect(url_for('index'))
        flash('Not correct data')
    return redirect(url_for('index'))


@app.post('/logout')
def logout():
    if current_user.is_authenticated:
        user = Users.query.filter_by(login=request.form['login']).first()
        if user and check_password_hash(user.psw, request.form['psw']):
            logout_user()
            session['userLogged'] = False
            flash("You've been logged out")
            return redirect(url_for('index'))
        flash('Not correct data')
        return redirect(url_for('index'))
    flash('You are not logged in')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False)
