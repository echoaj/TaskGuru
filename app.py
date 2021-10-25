from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h1>Welcome to my website about lightning.</h1>"


if __name__ == '__main__':
    app.run(debug=True)
