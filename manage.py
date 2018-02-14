from __future__ import print_function
from flask_script import Manager
from questions import app, db
from questions.models import User

manager = Manager(app)

# データベース作成
@manager.command
def init_db():
    db.create_all()
    user = User(name='administrator', _password='administrator')
    db.session.add(user)
    db.session.commit()

# データベース削除
@manager.command
def destroy_db():
    db.drop_all()

if __name__ == '__main__':
    manager.run()

