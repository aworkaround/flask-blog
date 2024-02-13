from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config['SECRET_KEY'] = 'my secret key'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(user_id):
    return Profiles.query.get(int(user_id))


class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(400), nullable=True)
    description = db.Column(db.Text, nullable=True)
    thumbnail = db.Column(db.String(180), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'profiles.id'), nullable=False)


class Profiles(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    blogs = db.relationship('Blogs', backref='author', lazy=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    blogs = Blogs.query.all()
    return render_template("index.html", blogs=blogs)


@app.route("/blog/<int:blog_id>")
def blog(blog_id):
    return f"<h1>This is Blog {blog_id}</h1>"


@app.route("/blog/create", methods=["GET", "POST"])
@login_required
def create_blog():
    if request.method == "POST":
        blog = Blogs(
            title=request.form.get("title"),
            subtitle=request.form.get("subtitle"),
            description=request.form.get("description"),
            thumbnail="img11.jpg",
        )
        db.session.add(blog)
        db.session.commit()
    return render_template("create_blog.html")


@app.route("/blog/edit/<int:blog_id>", methods=["GET", "POST"])
def edit_blog(blog_id):
    blog = Blogs.query.filter_by(id=blog_id).first()
    if not blog:
        return "<h1>404: Blog not found</h1>"
    if request.method == "POST":
        blog.title = request.form.get("title")
        blog.subtitle = request.form.get("subtitle")
        blog.description = request.form.get("description")
        blog.thumbnail = "img11.jpg"
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit_blog.html", blog=blog)


@app.route("/blog/delete/<int:blog_id>")
def delete_blog(blog_id):
    blog = Blogs.query.filter_by(id=blog_id).first()
    if blog:
        db.session.delete(blog)
        db.session.commit()
        return redirect(url_for("home"))
    return "<h1>404: Blog not found</h1>"


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if request.form.get("password") != request.form.get("cnf_password"):
            return '<h1>Passwords are not matching.</h1>'
        user = Profiles(
            email=request.form.get("email"),
            name=request.form.get("name"),
            password=request.form.get("password")
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Profiles.query.filter_by(email=request.form.get('email')).first()
        if user and (user.password == request.form.get('password')):
            login_user(user)
        else:
            return '<h1>Incorrect Credentials</h1>'
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')  

@app.route('/blogs')
def blogs():
    return 'All Blogs'


app.run(debug=True)
