from __future__ import print_function
from flask_script import Manager
from questions import app, db
from questions.models import User

manager = Manager(app)

# データベース初期化
# コマンドラインで　python manage.py init_db
@manager.command
def init_db():
    db.drop_all()
    db.create_all()
    user = User(name='administrator', password='administrator')
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    manager.run()

