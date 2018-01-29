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
        elif session.get('user_name') == 'admin':
            return redirect(url_for('show'))
        return f(*args, **kwargs)
    return decorated_view

def branchAB():
    r = random.randint(0, 1)
    if r == 0:
        return 'A'
    else:
        return 'B'

@app.route('/')
def top():
    header = ''
    footer = ''
    return render_template('top.html', header=header, footer=footer)

@app.route('/login', methods=['POST'])
def login():
    header = ''
    footer = ''
    uname = request.form['user_name']
    if db.session.query(Answer.user_name).filter(Answer.user_name==uname).count():
        flash('おかえりなさい' + uname + 'さん')
    else:
        answer = Answer(user_name = uname)
        for i in range(app.config['BRANCH_NUMBER']):
            answer.branch[i] = branchAB()
        db.session.add(answer)
        db.session.commit()
        flash('こんにちは' + uname + 'さん')
    session['user_name'] = uname
    return redirect(url_for('question'))

@app.route('/logout')
def logout():
    header = ''
    footer = ''
    session.pop('user_name', None)
    flash('ログアウトしました')
    return render_template('top.html')

@app.route('/question')
@login_required
def question():
    header = ''
    footer = ''
    user = db.session.query(Answer.user_name).filter(Answer.user_name==session.get('user_name'))
    return render_template('question.html', header=header, footer=footer, user=user)

@app.route('/answer', methods=['POST'])
@login_required
def answer():
    header = ''
    footer = ''
    answer = Answer(
            )
    db.session.add(answer)
    db.session.commit()
    flash('ご回答ありがとうございました！')
    return redirect(url_for('top'))

@app.route('/admin')
@login_required
def show():
    answers = Answer.query.all()
    header = '管理者ページ'
    footer = 'アンケート調査'
    return render_template('admin.html', answers = answers, header=header, footer=footer)

@app.route('/output', methods=['POST'])
@login_required
def output():
    f = open('questions/upload/output.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['id', 'q1', 'q2', 'type1', 'q3', 'q4', 'type2', 'q5', 'q6'])
    for answer in Answer.query.all():
        writer.writerow([answer.id, answer.q1, answer.q2, answer.type1, answer.q3, answer.q4, answer.type2, answer.q5, answer.q6])
    f.close()
    flash('更新しました')
    return redirect(url_for('show'))

@app.route('/download', methods=['POST'])
@login_required
def download():
    flash('')
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'output.csv', as_attachment=True)
