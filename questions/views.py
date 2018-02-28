import random, csv, codecs
from functools import wraps
from flask import request, redirect, url_for, render_template, flash, send_from_directory, session
from questions import app, db
from questions.models import Answer, User

def login_required(f):
    @wraps(f)
    def login_wrap(*args, **kwargs):
        if session.get('user_name') is None:
            return redirect(url_for('top'))
        return f(*args, **kwargs)
    return login_wrap

def auth_required(f):
    @wraps(f)
    def auth_wrap(*args, **kwargs):
        if session.get('administrator') is None:
            return redirect(url_for('auth'))
        return f(*args, **kwargs)
    return auth_wrap

def branchAB():
    if random.randint(0, 1) == 0:
        return 'A'
    else:
        return 'B'

@app.route('/')
def top():
    header = 'インターネット掲示板についてのアンケート調査'
    footer = ''
    return render_template('top.html', header=header, footer=footer)

@app.route('/login', methods=['POST'])
def login():
    uname = request.form['user_name']
    if db.session.query(Answer).filter(Answer.user_name==uname).count():
        flash('おかえりなさい' + uname + 'さん')
    else:
        answer = Answer(user_name = uname)
        for i in range(app.config['BRANCH_NUMBER']):
            exec('answer.branch%d = branchAB()' % (i))
        db.session.add(answer)
        db.session.commit()
        flash('こんにちは' + uname + 'さん')
    session.pop('user_name', None)
    session['user_name'] = uname
    return redirect(url_for('question'))

@app.route('/logout')
def logout():
    flash('ログアウトしました')
    if session.get('administrator'):
        session.pop('administrator', None)
        return redirect(url_for('auth'))
    session.pop('user_name', None)
    return redirect(url_for('top'))

@app.route('/question')
@login_required
def question():
    header = 'インターネット掲示板についてのアンケート調査'
    footer = ''
    uname = session.get('user_name')
    user = db.session.query(Answer).filter(Answer.user_name==uname).first()
    return render_template('question.html', header=header, footer=footer, user=user)

@app.route('/answer', methods=['POST'])
@login_required
def answer():
    answer = db.session.query(Answer).filter(Answer.user_name==session.get('user_name')).first()
    for i in range(app.config['QUESTION_NUMBER']):
        exec('answer.question%d = request.form[\'q\' + str(i)] ' % (i))
    db.session.add(answer)
    db.session.commit()
    flash('ご回答ありがとうございました！')
    return redirect(url_for('top'))

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    header = '管理画面 - インターネット掲示板についてのアンケート調査'
    footer = ''
    administrator = db.session.query(User).first()
    if request.method == 'POST':
        if administrator.name == request.form['name'] and administrator.password == request.form['password']:
            session['administrator'] = True
            return redirect(url_for('show'))
        else:
            flash('管理者名またはパスワードが間違っています')
    return render_template('auth.html', header=header, footer=footer)

@app.route('/admin')
@auth_required
def show():
    answers = Answer.query.all()
    header = '管理画面 - インターネット掲示板についてのアンケート調査'
    footer = ''
    return render_template('admin.html', answers = answers, header=header, footer=footer)

@app.route('/output', methods=['POST'])
@auth_required
def output():
    # csv書き込みの準備
    f = open('/tmp/output.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    # csv1行目
    csv_row_name = ['id', 'user_name']
    for i in range(app.config['BRANCH_NUMBER']):
        csv_row_name.append('branch' + str(i))
    for i in range(app.config['QUESTION_NUMBER']):
        csv_row_name.append('question' + str(i))
    writer.writerow(csv_row_name)
    # csvにデータベースから書き出す
    for answer in Answer.query.all():
        csv_row = [answer.id, answer.user_name]
        for i in range(app.config['BRANCH_NUMBER']):
            exec('csv_row.append(answer.branch%d)' % (i))
        for i in range(app.config['QUESTION_NUMBER']):
            exec('csv_row.append(answer.question%d)' % (i))
        writer.writerow(csv_row)
    f.close()
    flash('更新しました')
    return redirect(url_for('show'))

@app.route('/download', methods=['POST'])
@auth_required
def download():
    return send_from_directory('/tmp/', 'output.csv', as_attachment=True)

@app.route('/change', methods=['POST'])
@auth_required
def change():
    if request.form.get('_method') == 'PUT':
        administrator = db.session.query(User).first()
        if administrator.password == request.form['old']:
            if request.form['new'] == request.form['confirm']:
                administrator.password = request.form['new'] 
                db.session.add(administrator)
                db.session.commit()
                flash('パスワードを変更しました')
                return redirect(url_for('show'))
            else:
                flash('新しいパスワードが確認用入力欄と一致しませんでした')
                return redirect(url_for('show'))
        else:
            flash('元のパスワードが正しくありませんでした、ログインからやり直してください')
    return redirect(url_for('auth'))

# データベース初期化
@app.route('/destroy', methods=['POST'])
@auth_required
def destroy():
    if request.form.get('_method') == 'DELETE':
        db.drop_all()
        db.create_all()
        user = User(name='administrator', password='administrator')
        db.session.add(user)
        db.session.commit()
        flash('新規作成しました')
    return redirect(url_for('auth'))
