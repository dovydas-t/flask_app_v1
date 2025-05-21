

from functools import wraps
from flask import Flask, flash, render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from config import database_url
from flask_migrate import Migrate
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(35), unique=True, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    vin = db.Column(db.String(17), unique=True, nullable=False)

    posts = db.relationship('Post', backref='creator', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', User ID: {self.user_id})"



def login_required(f):
    @wraps(f)
    def decodated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decodated_function





@app.route('/')
def index():
    return render_template('index.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data
        email = form.email.data
        birth_date = form.birth_date.data
        vin = form.vin.data
        
        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            password_hash=hashed_password,
            name=name,
            email=email,
            birth_date=birth_date,
            vin=vin
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash(f"Account created for {new_user.username}!", "success")
        return redirect(url_for('login'))  # Change to a success page if needed
    
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        query = db.select(User).filter_by(username=username)
        user_result = db.session.execute(query).first()
        if user_result is None:
            flash("User not found", "error")
            return render_template('login.html', form = form)
        user : User = user_result[0]
        if check_password_hash(user.password_hash, password):
            session.permanent = True
            session["user_id"] = user.id
            session["username"] = user.username

            flash("User is logged in", "success")
            return redirect(url_for('index'))
        

        flash("Incorect password", "error")
        return render_template('login.html', form = form)
    
    return render_template('login.html', form = form)

@app.route('/posts')
def all_posts():
    if posts in Post.query.order_by(Post.created_at.desc()).all():
        if 'user_id' in session:
                user_posts = user.posts
                if not user_posts:
                    flash("This user has no posts", "info")
    else:
        flash("No posts available", "info")


    posts = Post.query.order_by(Post.created_at.desc()).all()
    if not posts:
        flash("No posts available", "info")

    user = User.query.get(session["user_id"])
    if user:        
        user_posts = user.posts
        if not user_posts:
            flash("This user has no posts", "info")
    if 'user_id' in session:
        user = User.query.get(session["user_id"])
        flash("User not logged in", "warning")
    return render_template('posts.html', posts=posts, user_posts=user_posts)


@app.route('/system')
@login_required
def system():
    return render_template('system.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("User is logged out", "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
