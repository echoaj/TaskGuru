from flask import Flask

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return "<h1>Welcome to Task Guru  --version Final.</h1>"


if __name__ == '__main__':
    app.run()
