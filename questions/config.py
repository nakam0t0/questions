DEBUG = False
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/questions.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 以下、適宜変更の必要あり

# セッション（短い記録）の保持に必要なkey
SECRET_KEY = 'Polarizationから変更の必要あり'
# 分岐の数
BRANCH_NUMBER = 1
# 質問（保存する回答）の数
QUESTION_NUMBER = 30
