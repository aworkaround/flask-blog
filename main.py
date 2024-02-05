from flask import Flask, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

db = SQLAlchemy(app)


class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(400), nullable=True)
    description = db.Column(db.Text, nullable=True)
    thumbnail = db.Column(db.String(180), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    blogs = Blogs.query.all()
    return render_template("index.html", blogs=blogs)


@app.route("/blog/<int:blog_id>")
def blog(blog_id):
    return f"<h1>This is Blog {blog_id}</h1>"


@app.route("/blog/create")
def create_blog():
    blog = Blogs(title="Blog 1", subtitle="Subtitle of blog 1", thumbnail="img11.jpg")
    db.session.add(blog)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/blog/delete/<int:blog_id>")
def delete_blog(blog_id):
    blog = Blogs.query.filter_by(id=blog_id).first()
    if blog:
        db.session.delete(blog)
        db.session.commit()
        return redirect(url_for("home"))
    return "<h1>404: Blog not found</h1>"


app.run(debug=True)
