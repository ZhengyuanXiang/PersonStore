from . import redis_conn, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

KEY_USER_INFO = 'User_INFO_'
KEY_USER_ID_TO_EMAIL = 'User_ID_TO_EMAIL_'
KEY_USER_ID = 'UserID'


class User(UserMixin):
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.id = None

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def query_by_email(email):
        if not email:
            return None
        u = redis_conn.hgetall(KEY_USER_INFO + email)
        if not len(u):
            return None

        new_user = User(u['Email'], u['Name'], u['Password'])
        new_user.id = u['Id']
        return new_user

    def add_user(self):
        id = redis_conn.incr(KEY_USER_ID)
        redis_conn.watch(self.email)
        u = redis_conn.hgetall(self.email)
        if len(u):
            redis_conn.unwatch()
            return False

        pipe = redis_conn.pipeline()
        pipe.hmset(KEY_USER_INFO + self.email,
                   {'Id': id, 'Name': self.username, 'Password': self.password_hash, 'Email': self.email})

        pipe.set(KEY_USER_ID_TO_EMAIL + str(id), self.email)

        ret = pipe.execute()[0]
        if not ret:
            return False

        return True


@login_manager.user_loader
def load_user(user_id):
    email = redis_conn.get(KEY_USER_ID_TO_EMAIL + str(user_id))
    return User.query_by_email(email)

