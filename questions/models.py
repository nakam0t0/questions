from questions import app, db

# データベースに関する定義

# 回答に関するテーブルの定義 
# idはデータの操作に必須 
# user_nameにはクラウドワークスののユーザ名を保存
# branchには質問をランダムで分けた分岐結果（AかB）を保存
# questionには回答（整数）を保存 
# branchはquestionと連動していない
class Answer(db.Model):
    branch = {} 
    question = {}
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text)
    for i in range(app.config['BRANCH_NUMBER']):
        branch[i] = db.Column(db.Text)
    for i in range(app.config['QUESTION_NUMBER']):
        question[i] = db.Column(db.Text)

# データベース作成
def init():
    db.create_all()

# データベース削除
def destroy():
    db.drop_all()
