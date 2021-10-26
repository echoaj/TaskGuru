from flask import Flask, render_template
from flaskr import app


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
