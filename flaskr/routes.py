from flask import render_template, url_for, request, redirect, flash
from flaskr.forms import SignUpForm, LoginForm
from flaskr import app, db, bcrypt
from flaskr.models import User, Todo
from flask_login import logout_user, login_user, current_user, login_required


# without 'POST' we get when adding something Method Not Allowed error
# without 'GET' we get Method Not Allowed at startup
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# without 'POST' we don't get an error
# without 'GET' we get Method Not Allowed at startup
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for("account"))
    except:
        return "<h1>Cannot commit at this time</h1>"


# without 'POST' we get Method Not Allowed error after updating on update page
# without 'GET' we get Method Not Allowed when pressing update on index page
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_to_update.content=request.form['content']
        try:
            db.session.commit()
            return redirect(url_for("account"))
        except:
            return "<h1>Cannot commit at this time</h1>"
    else:
        return render_template('/update.html', task=task_to_update)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = SignUpForm()
    if form.validate_on_submit():
        # convert password to hash and decode it from bytes to string
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Success! Account created for {form.username.data}!', category='success')
        return redirect(url_for('login'))
    return render_template('/signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # check if user exists, and password the entered in matches the password in database
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)  # logs in user and remembers pass
            next_page = request.args.get('next')  # after loggin in it will redirect you to the page you where trying to access before hand
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('account'))
        else:
            flash('Log in unsuccessful. Please check email and password.', category='danger')
        return redirect(url_for('account'))
    return render_template('/login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return render_template('/index.html')


@app.route('/account', methods=['GET', 'POST'])
@login_required             # extension knows we must login in order to access this route
def account():
    if request.method == 'POST':
        task_content = request.form['content']
        print(task_content)
        print(current_user.id)
        new_task = Todo(content=task_content, user_id=current_user.id)
        print(new_task.id)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for("account"))  # or can say redirect('/')
        except:
            return "There was a problem. Record was not added"
    else:
        # filter taks by user and order by data created .filter_by(id=current_user.id)
        if current_user.email == "admin@gmail.com":
            tasks = Todo.query.order_by(Todo.date_created).all()
        else:
            tasks = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.date_created).all()
        return render_template('account.html', tasks=tasks)
