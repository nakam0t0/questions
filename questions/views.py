import random, csv, codecs
from functools import wraps
from flask import request, redirect, url_for, render_template, flash, send_from_directory, session
from questions import app, db
from questions.models import Answer

def login_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if session.get('user_name') is None:
            return redirect(url_for('top'))
        return f(*args, **kwargs)
    return decorated_view

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
    session.pop('user_name', None)
    flash('ログアウトしました')
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

@app.route('/admin')
@login_required
def show():
    answers = Answer.query.all()
    data = {}
    header = '管理画面 - インターネット掲示板についてのアンケート調査'
    footer = ''
    return render_template('admin.html', answers = answers, header=header, footer=footer)

@app.route('/output', methods=['POST'])
@login_required
def output():
    # csv書き込みの準備
    f = open('questions/upload/output.csv', 'w')
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
@login_required
def download():
    flash('')
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'output.csv', as_attachment=True)
