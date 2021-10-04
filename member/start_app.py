from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "rlarldyd"   #비밀키 설정

def getconn():
    conn = sqlite3.connect("c:/webdb/webdb.db")
    return conn

# index() 페이지
@app.route('/')
def main():
    if 'userID' in session:  # 세션에 userID 이름이 있으면(로그인이 됐다면)
        return render_template("main.html", username=session.get('userID'), login=True)
    else:
        return render_template('main.html', login=False)

# 회원 목록
@app.route('/memberlist')
def memberlist():
    # DB 연동
    #conn = sqlite3.connect("c:/webdb/webdb.db")
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member"
    cur.execute(sql)
    rs = cur.fetchall()
    #print(rs)
    conn.close()
    if 'userID' in session:
        return render_template('memberlist.html', rs=rs, username=session.get('userID'), login=True)
    else:
        return render_template('memberlist.html', login=False)

# 회원 등록
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 데이터 가져오기(웹페이지)
        id = request.form['memberid']
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']
        date = request.form['reg_date']

        #DB 연동
        #conn = sqlite3.connect("c:/webdb/webdb.db")
        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO member VALUES ('%s', '%s', '%s', '%s', '%s')" % (id, pwd, name, age, date)
        cur.execute(sql)
        conn.commit()
        conn.close()

        return redirect(url_for('main')) # 강제로 주소(페이지) 이동

    else:
        return render_template('register.html')

# 회원 상세 보기 - 1명
@app.route('/member_view/<string:id>')
def member_view(id):
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE memberid = '%s' " % (id)
    cur.execute(sql)
    rs = cur.fetchone()
    print(rs)
    conn.close()
    if "userID" in session:
        return render_template('member_view.html', rs=rs, username=session.get('userID'), login=True)
    else:
        return render_template('member_view.html', login = False)

# 회원 로그인
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
       # 입력상자의 데이터 가져오기
        id = request.form['memberid']
        pwd = request.form['passwd']

       # DB의 회원과 비교
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE memberid = '%s' AND passwd = '%s' " % (id, pwd)
        cur.execute(sql)
        rs = cur.fetchone()
        print(rs)
        if rs:  #로그인이 되면 메인 페이지로 이동
            # 세션 발급 (세션이름 - userID)
            session['userID'] = id
            return redirect(url_for('main'))
        else:  #로그인이 안되면 에러메시지를 출력하고 다시 로그인
            error = "아이디나 비밀번호가 일치하지 않습니다."
            return render_template("login.html", error = error)
    else:
        return render_template("login.html")

# 회원 로그아웃
@app.route('/logout')
def logout():
    session.pop('userID') # 세션 삭제
    return redirect(url_for('main'))

# 회원 삭제
@app.route('/member_delete/<string:id>')
def member_delete(id):
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM member WHERE memberid = '%s' " % (id)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return redirect(url_for('memberlist'))

# 회원 수정
@app.route('/member_edit/<string:id>', methods = ['GET', 'POST'])
def member_edit(id):
    if request.method == 'POST':
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']
        date = request.form['reg_date']

        conn = getconn()
        cur = conn.cursor()
        sql = "UPDATE member SET passwd = '%s', name ='%s', age ='%s', reg_date='%s' WHERE memberid = '%s' " % (pwd, name, age, date, id)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(url_for('member_view', id=id))

    else:
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE memberid = '%s' " % (id)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
        return render_template('member_edit.html', rs=rs)

app.run()