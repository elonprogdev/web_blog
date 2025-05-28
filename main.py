from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET"])
def index():
    posts = session.get("posts", [])
    posts_with_index = list(enumerate(posts))  # Индексы заранее
    return render_template("index.html", posts=posts_with_index)


@app.route("/add", methods=["POST"])
def add_post():
    title = request.form.get("title")
    description = request.form.get("description")
    image = request.files.get("image")

    if image and title and description:
        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)

        post = {
            "title": title,
            "description": description,
            "image_url": "/" + filepath.replace("\\", "/"),
            "likes": 0
        }

        posts = session.get("posts", [])
        posts.insert(0, post)  # новые сверху
        session["posts"] = posts

    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(debug=True)