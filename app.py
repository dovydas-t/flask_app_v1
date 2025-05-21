

from functools import wraps
from flask import Flask, flash, render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from config import database_url
from flask_migrate import Migrate
from forms import LoginForm, RegisterForm, RegisterDetailsForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'index'
bcrypt = Bcrypt(app)


# Database Models
class AuthUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    profile = db.relationship('UserProfile', backref='auth_user', uselist=False)
    posts = db.relationship('Post', backref='creator', lazy=True)

    def __repr__(self):
        return f"AuthUser('{self.id}', '{self.username}')"

class UserProfile(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('auth_user.id'), primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(35), unique=True, nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return f"UserProfile('{self.id}', '{self.created_at}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', User ID: {self.user_id})"

@login_manager.user_loader
def load_user(user_id):
    return AuthUser.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = AuthUser.query.filter_by(username=username).first()

        if user:
            flash("Username already exists", "error")
            return render_template('register.html', form=form)
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = AuthUser(username=username, password_hash=hashed_password)
        user_profile = UserProfile(name=None, email=None, birth_date=None)

        #FIXME: Maybe needs to be changed to user_profile = UserProfile()
        new_user.profile = user_profile
        #user_profile = UserProfile(id=new_user.id, name=None, email=None, birth_date=None)
        #db.session.add(user_profile)
        #db.session.commit()

        db.session.add(new_user)
        db.session.commit()
        flash(f"Account created for {new_user.username}!", "success")
        return redirect(url_for('login'))
    
    return render_template("register.html", form=form)

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        user = AuthUser.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            flash(f"Welcome back, {user.username}!", "success")
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password", "error")
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/profile')
@login_required
def profile():
    user = AuthUser.query.get(current_user.id)
    if user:
        return render_template('profile.html', user=user)
    else:
        flash("User not logged in", "error")
        return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("User logged out", "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
