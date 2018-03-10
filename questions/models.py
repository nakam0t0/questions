from questions import app, db

# データベースに関する定義

'''
回答に関するテーブルの定義 
idはデータの操作に必須 
user_nameにはクラウドワークスののユーザ名を保存
branchには質問をランダムで分けた分岐結果（AかB）を保存
questionには回答（整数）を保存 
branchはquestionと連動していない
branch, question共に直後に０始まりの番号が振られる

分岐数、質問数はconfig.pyの値を受ける
'''
class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text)
    for i in range(app.config['BRANCH_NUMBER']):
        exec('branch%d = db.Column(db.Text)' % (i))
    for i in range(app.config['QUESTION_NUMBER']):
        exec('question%d = db.Column(db.Text)' % (i))

# 管理者の認証のためのテーブル
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    password = db.Column('password', db.Text)

# データベース初期化
def init():
    db.drop_all()
    db.create_all()
    user = User(name='administrator', password='administrator')
    db.session.add(user)
    db.session.commit()
