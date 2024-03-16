from flask import Flask, flash, redirect, render_template, url_for, request
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = '301bafebd87884dedb1e0811c457880d'

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
    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    blogs = db.relationship('Blogs', backref='author', lazy=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    page_no = int(request.args.get('page')) if request.args.get('page') else 1
    blogs = Blogs.query.paginate(page=page_no, max_per_page=6)
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
            user_id = current_user.id
        )
        db.session.add(blog)
        db.session.commit()
        flash('Blog successfully created!', 'success')
    return render_template("create_blog.html")


@app.route("/blog/edit/<int:blog_id>", methods=["GET", "POST"])
@login_required
def edit_blog(blog_id):
    blog = Blogs.query.filter_by(id=blog_id).first()
    if current_user.id != blog.author.id:
        flash('You are unauthorized to perform this operation', 'error')
        return redirect(url_for('home'))
    if not blog:
        return "<h1>404: Blog not found</h1>"
    if request.method == "POST":
        blog.title = request.form.get("title")
        blog.subtitle = request.form.get("subtitle")
        blog.description = request.form.get("description")
        blog.thumbnail = "img11.jpg"
        db.session.commit()
        flash('Blog successfully edited!', 'success')
        return redirect(url_for('home'))
    return render_template("edit_blog.html", blog=blog)


@app.route("/blog/delete/<int:blog_id>")
@login_required
def delete_blog(blog_id):
    blog = Blogs.query.filter_by(id=blog_id).first()
    if current_user.id != blog.author.id:
        flash('You are unauthorized to perform this operation', 'error')
        return redirect(url_for('home'))
    if blog:
        db.session.delete(blog)
        db.session.commit()
        flash('Blog successfully deleted!', 'success')
        return redirect(url_for("home"))
    return "<h1>404: Blog not found</h1>"


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/blogs")
def blogs():
    return render_template("blogs.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = Profiles(
            full_name=request.form.get("full_name"),
            password=request.form.get("password"),
            email=request.form.get("email")
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('New used created successfully. You are logged now!', 'success')
        return redirect(url_for('home'))
    return render_template("signup.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    next_page = request.args.get('next')
    if request.method == "POST":
        user = Profiles.query.filter_by(
            email=request.form.get("email")).first()
        if not user:
            flash('User does not exist!', 'error')
            return render_template("login.html")
        if request.form.get('password') == user.password:
            login_user(user)
            if next_page: 
                return redirect(next_page)
            flash('You are logged now!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect Credentials!', 'error')
            return render_template("login.html")
    if next_page:
        flash('You need to be logged in first!', 'info')
    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out successfully!', 'success')
    return redirect(url_for('home'))


app.run(debug=True)
