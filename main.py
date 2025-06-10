from flask import Flask, render_template, request, redirect, url_for, session
import os
import uuid



app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

users = {}  # {login: password}
likes = {}



@app.route("/")
def index():
    posts = session.get("posts", [])
    posts_with_index = list(enumerate(posts))
    return render_template("index.html", posts=posts_with_index, user=session.get("user"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        if login and password and login not in users:
            users[login] = password
            session["user"] = login
            return redirect(url_for("index"))
        else:
            return "Пользователь уже существует или данные некорректны"
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        if login in users and users[login] == password:
            session["user"] = login
            return redirect(url_for("index"))
        else:
            return "Неверный логин или пароль"
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route("/add", methods=["POST"])
def add_post():
    if "user" not in session:
        return redirect(url_for("login"))

    title = request.form.get("title")
    description = request.form.get("description")
    image = request.files.get("image")

    if image and title and description:
        ext = os.path.splitext(image.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)

        post = {
            "title": title,
            "description": description,
            "image_url": "/" + filepath.replace("\\", "/"),
            "likes": 0,
            "liked_by": []
        }

        posts = session.get("posts", [])
        posts.insert(0, post)
        session["posts"] = posts

    return redirect(url_for("index"))


@app.route("/like/<int:index>", methods=["POST"])
def like_post(index):
    if "user" not in session:
        return redirect(url_for("login"))

    user = session["user"]
    posts = session.get("posts", [])

    if 0 <= index < len(posts):
        like_key = (user, index)
        if not likes.get(like_key):
            posts[index]["likes"] += 1
            posts[index].setdefault("liked_by", []).append(user)
            likes[like_key] = True
            session["posts"] = posts

    return redirect(url_for("index"))

@app.route("/comment/<int:index>", methods=["POST"])
def comment_post(index):
    if "user" not in session:
        return redirect(url_for("login"))

    comment_text = request.form.get("comment")
    if not comment_text:
        return redirect(url_for("index"))

    posts = session.get("posts", [])
    if 0 <= index < len(posts):
        posts[index].setdefault("comments", [])
        posts[index]["comments"].append({
            "author": session["user"],
            "text": comment_text
        })
        session["posts"] = posts

    return redirect(url_for("index"))




if __name__ == "__main__":
    app.run(debug=True)