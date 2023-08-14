from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    collections = db.relationship('Collection', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tasks = db.relationship('Task', backref='collection', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    enabled = db.Column(db.Boolean, default=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(64), default='not started')
    spent_time = db.Column(db.Integer, default=0)
    pause_time = db.Column(db.Integer, default=0)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))

    def start(self):
        if self.status in ['not started', 'paused']:
            self.status = 'in progress'
            self.start_time = datetime.utcnow()

    def pause(self):
        if self.status == 'in progress':
            self.status = 'paused'
            self.spent_time += (
                (datetime.utcnow() - self.start_time)
                .total_seconds()
            )
            self.pause_time = int(self.spent_time)

    def complete(self):
        if self.status in ['completed', 'not started']:
            return
        if self.status == 'in progress':
            self.spent_time += (
                (datetime.utcnow() - self.start_time)
                .total_seconds()
            )
        self.status = 'completed'
        self.end_time = datetime.utcnow()

    def get_spent_time(self):
        total_seconds = int(self.spent_time)
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{hours:02}:{minutes:02}:{seconds:02}"
