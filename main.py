from flask import Flask, render_template, request, url_for, redirect


app = Flask(__name__)



@app.route("/", methods=["GET"])
def index():
    if request.args.get('name') and request.args.get('age'):
        return render_template("index.html", user_name = request.args.get('name'), user_age = "("+ request.args.get('age') + ")")
    else:
        return render_template("index.html")
        







if __name__ == "__main__":
    app.run(debug=True)