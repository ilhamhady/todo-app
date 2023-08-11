from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Task, Collection, User
from datetime import timedelta
import os

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SECRET_KEY'] = os.urandom(24)
db.init_app(app)

with app.app_context():
    # db.drop_all()
    db.create_all()


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('signin'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    collections = user.collections.all()

    for collection in collections:
        collection.created_at = get_local_time(collection.created_at)

    return render_template('index.html', collections=collections, username=user.username, popup_closed=session.get('popup_closed', False))


@app.route('/collection', methods=['POST'])
def create_collection():
    if 'user_id' not in session:
        return redirect(url_for('signin'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    name = request.form.get('name')
    collection = Collection(name=name, user=user, enabled=True)
    db.session.add(collection)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/collection/<int:collection_id>/task', methods=['POST'])
def create_task(collection_id):
    if 'user_id' not in session:
        return redirect(url_for('signin'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    collection = user.collections.filter_by(id=collection_id).first()
    if not collection:
        flash('Invalid collection ID or you do not have permission to access this collection.')
        return redirect(url_for('index'))

    title = request.form.get('title')
    task = Task(title=title, collection=collection)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/collection/<int:collection_id>/toggle', methods=['POST'])
def toggle_collection(collection_id):
    if 'user_id' not in session:
        return redirect(url_for('signin'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    collection = user.collections.filter_by(id=collection_id).first()
    if not collection:
        return '', 403  # Return 403 Forbidden status code

    collection.enabled = not collection.enabled
    db.session.commit()
    return '', 204  # Return 204 No Content status code


@app.route('/task/<int:task_id>/start', methods=['POST'])
def start_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.start()
        return redirect(url_for('index'))
    else:
        flash('Invalid task ID.')
        return redirect(url_for('index'))


@app.route('/task/<int:task_id>/pause', methods=['POST'])
def pause_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.pause()
        return redirect(url_for('index'))
    else:
        flash('Invalid task ID.')
        return redirect(url_for('index'))


@app.route('/task/<int:task_id>/done', methods=['POST'])
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.complete()
        return redirect(url_for('index'))
    else:
        flash('Invalid task ID.')
        return redirect(url_for('index'))


@app.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.collection.user.id == session['user_id']:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        flash('Invalid task ID or not authorized.')
        return redirect(url_for('index'))


@app.route('/collection/<int:collection_id>/delete', methods=['POST'])
def delete_collection(collection_id):
    collection = Collection.query.get(collection_id)
    if collection and collection.user.id == session['user_id']:
        db.session.delete(collection)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        flash('Invalid collection ID or not authorized.')
        return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is not None:
            flash('Username already exists.')
            return redirect(url_for('signup'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('You have signed up successfully.')
        return redirect(url_for('signin'))
    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password.')
            return redirect(url_for('signin'))
        session['user_id'] = user.id
        return redirect(url_for('index'))
    return render_template('signin.html')


@app.route('/signout')
def signout():
    session.pop('user_id', None)
    session['popup_closed'] = False
    flash('You have been signed out.')
    return redirect(url_for('signin'))


@app.route('/close-popup', methods=['POST'])
def close_popup():
    session['popup_closed'] = True
    return '', 204


@app.route('/set_timezone_offset', methods=['POST'])
def set_timezone_offset():
    session['timezone_offset'] = int(request.form.get('offset'))
    return '', 204  # Return 204 No Content status code


def get_local_time(utc_time):
    offset = session.get('timezone_offset', 0)
    local_time = utc_time - timedelta(minutes=offset)
    return local_time


if __name__ == "__main__":
    app.run(debug=True)
