from flask import Flask, render_template

app = Flask(__name__)

blogs = [
    {
        "title": "This is a Blog 1",
        "subtitle": "This is subtitle of the blog",
        "description": "This is the description of my new blog",
        "thumbnail": "img11.jpg",
        "id": 1,
    },
    {
        "title": "This is a Blog 2",
        "subtitle": "This is subtitle of the blog",
        "description": "This is the description of my new blog",
        "thumbnail": "img11.jpg",
        "id": 2,
    },
]


@app.route("/")
def home():
    return render_template("index.html", blogs=blogs)


@app.route("/blog/<int:blog_id>")
def blog(blog_id):
    return f"<h1>This is Blog {blog_id}</h1>"


app.run(debug=True)
