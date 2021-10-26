from flaskr import app


@app.route("/")
@app.route("/home")
def home():
    return "<h1>Welcome to Task Guru :) :)</h1>"


if __name__ == '__main__':
    app.run()
