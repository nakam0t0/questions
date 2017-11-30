import random, csv, codecs
from flask import request, redirect, url_for, render_template, flash, send_from_directory # send_file
from questions import app, db
from questions.models import Answer

def arrangeAB(column):
    a_num = Answer.query.filter(column == "A").count()
    b_num = Answer.query.filter(column == "B").count()
    if a_num > b_num:
        return "B"
    elif a_num < b_num:
        return "A"
    else:
        r = random.randint(0, 1)
        if r == 0:
            return "A"
        elif r == 1:
            return "B"
        else:
            print("おかしい")

@app.route('/')
def question():
    type1 = arrangeAB(Answer.type1)
    type2 = arrangeAB(Answer.type2)
    a1 = Answer.query.filter(Answer.type1 == "A").count()
    b1 = Answer.query.filter(Answer.type1 == "B").count()
    a2 = Answer.query.filter(Answer.type2 == "A").count()
    b2 = Answer.query.filter(Answer.type2 == "B").count()
    header = "アンケートにご協力お願いします"
    return render_template('question.html', header=header, type1=type1, type2=type2, a1=a1, b1=b1, a2=a2, b2=b2)

@app.route('/answer', methods=['POST'])
def answer():
    answer = Answer(
            q1 = request.form['q1'],
            q2 = request.form['q2'],
            type1 = request.form['type1'],
            q3 = request.form['q3'],
            type2 = request.form['type2'],
            q4 = request.form['q4'],
            q5 = request.form['q5'],
            q6 = request.form['q6'],
            )
    db.session.add(answer)
    db.session.commit()
    flash('ご回答ありがとうございました！')
    return redirect(url_for('question'))

@app.route('/admin')
def show():
    answers = Answer.query.all()
    header = "管理者ページ"
    return render_template('admin.html', answers = answers, header=header)

@app.route('/output', methods=['POST'])
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
def download():
    return send_from_directory(app.config['UPLOAD_FOLDER'], "output.csv", as_attachment=True)
    # return redirect(url_for('show'))
