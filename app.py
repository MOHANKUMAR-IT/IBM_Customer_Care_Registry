
import email
from tkinter.messagebox import NO
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import time

app = Flask(__name__)

app.secret_key = 'StrongPixel1090!'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'customer_care_registry'

mysql = MySQL(app)

@app.route('/')
@app.route('/index')
def landing_page():
    if(len(session)>0):
        return render_template("index.html")
    else:
        redirect('/login')



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('session_id', None)
    session.pop('user_name', None)
    session.pop('first_name',None)
    session.pop('last_name',None)
    session.pop('email_id',None)
    
    return redirect(url_for('login'))

@app.route('/adminlogin',methods=['GET','POST'])
def loginAdmin():
    msg = ''
    # print("came in")
    if request.method == 'POST' and 'email_id' in request.form and 'password' in request.form:
        # print(request.form)
        email_id = request.form['email_id']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_accounts WHERE email_id LIKE %s AND password LIKE %s', [email_id, password])
        account = cursor.fetchone()
        # print(account)
        if account:
            session['loggedin'] = True
            session['session_id'] = hash(account['email_id']+str(hash(account['password']+str(time.time()))))
            session['email_id'] = account['email_id']
            session['user_name'] = account['user_name']
            session['first_name'] = account['first_name']
            session['last_name'] = account['last_name']
            return redirect('index')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    # print("came in")
    if request.method == 'POST' and 'email_id' in request.form and 'password' in request.form:
        # print(request.form)
        email_id = request.form['email_id']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_accounts WHERE email_id LIKE %s AND password LIKE %s', [email_id, password])
        account = cursor.fetchone()
        # print(account)
        if account:
            session['loggedin'] = True
            session['session_id'] = hash(account['email_id']+str(hash(account['password']+str(time.time()))))
            session['email_id'] = account['email_id']
            session['user_name'] = account['user_name']
            session['first_name'] = account['first_name']
            session['last_name'] = account['last_name']
            return redirect('index')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    # print(list(request.form))
    if request.method == 'POST' and 'first_name' in request.form and 'password' in request.form and 'email_id' in request.form and 'last_name' in request.form and 'pno' in request.form and 'user_name' in request.form :
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        email_id = request.form['email_id']
        user_name = request.form['user_name']
        pno = request.form['pno']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # print(cursor)
        cursor.execute('SELECT * FROM user_accounts WHERE email_id LIKE %s', [email_id])
        account = cursor.fetchone()
        if account: 
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
            msg = 'Invalid email address !'
        elif not first_name or not last_name or not password or not email_id or not pno or not user_name:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user_accounts VALUES (% s, % s, % s , % s , % s , % s )', ( email_id ,user_name,password,pno,first_name,last_name))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            redirect('/login')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/register-issue',methods=['POST'])
def registerIssue():
    if request.method == 'POST' and 'title' in request.form and 'description' in request.form:
        title = request.form['title']
        desciption = request.form['description']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO issue_db(email_id,title,description) VALUES(%s,%s,%s)',(session['email_id'],title,desciption))
        mysql.connection.commit()
        return 'Issue ticket created successfully'




# for admin controls-------------------------------------------------------------------

@app.route('/admin',methods=['POST','GET'])
def admin():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT agent_id,email_id,solved_issues,pending_issues,profilepic,name FROM agent_accounts')
    account = cursor.fetchall()
    cursor.execute('SELECT * FROM issue_db where solved=0')
    issues = cursor.fetchall()
    return render_template('admin.html',agents=account,name="mohan",issues=issues)


@app.route('/new-agent-register',methods=['POST'])
def newAgentRegister():
    if 'name' in request.form and 'email_id' in request.form and 'password' in request.form:
        name = request.form['name']
        email_id = request.form['email_id']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO agent_accounts(name,email_id,password) VALUES(%s,%s,%s)',(name,email_id,password))
        mysql.connection.commit()
        return 'New Agent Created Successfully'
    return 'Error creating new agent'

@app.route('/assign-job-to-agent',methods=['POST'])
def assignJobToAgent():
    if 'agent_id' in request.form and 'ticket' in request.form:
        agent_id = request.form['agent_id']
        ticket = request.form['ticket']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE issue_db SET agent_id=%s AND pending_issues=pending_issues+1 WHERE ticket=%s',(agent_id,ticket))
        mysql.connection.commit()
        return 'New Job Assigned to agent %s',agent_id
    return 'Error Assigning Job to Agent'



# app.run(use_reloader=True)
if __name__ == '__main__':
    # from livereload import Server
    # server = Server(app.wsgi_app)
    app.run(debug=True)
    app.run()
    # server.serve(host = '0.0.0.0',port=5000)
    