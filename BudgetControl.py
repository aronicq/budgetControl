from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    user = {'nickname': "nick"}
    return render_template("index.html", title = "home", user = user)


if __name__ == '__main__':
    app.run()
