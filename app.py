
import email
from tkinter.messagebox import NO
from turtle import pen
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = "StrongPixel1090"
app.config['SESSION_TYPE'] = 'filesystem'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fgp33793;PWD=DXgCxphsnaCXNucS",'','')


@app.route('/')
@app.route('/index')
def landing_page():
    if session.get("email_id"):
        pending_issue_data = []
        sql = 'SELECT ticket,title,agent_id,progress FROM issue_db WHERE email_id= ? AND solved=0'
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,session['email_id'])
        ibm_db.execute(stmt)
        data = ibm_db.fetch_assoc(stmt)
        pending_issue_headings = []
        print('hello',data)
        if data:
            pending_issue_data.append(data)
            pending_issue_headings = data.keys()
        return render_template("index.html",pending_issue_data=pending_issue_data,pending_issue_headings=pending_issue_headings)
    else:
        return render_template('login.html')



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
        sql = 'SELECT * FROM user_accounts WHERE email_id LIKE ? AND password LIKE ?'
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email_id)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        # print(account)
        if account:
            session['loggedin'] = True
            session['session_id'] = hash(account['email_id']+str(hash(account['password']+str(time.time()))))
            session['email_id'] = account['EMAIL_ID']
            session['user_name'] = account['USER_NAME']
            session['first_name'] = account['FIRST_NAME']
            session['last_name'] = account['LAST_NAME']
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
        print(email_id,password)
        sql = 'SELECT * FROM user_accounts WHERE EMAIL_ID = ? AND PASSWORD = ?'

        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email_id)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            session['loggedin'] = True
            session['session_id'] = hash(account['EMAIL_ID']+str(hash(account['PASSWORD']+str(time.time()))))
            session['email_id'] = email_id
            session['user_name'] = account['USER_NAME']
            print(session)
            session['first_name'] = account['FIRST_NAME']
            session['last_name'] = account['LAST_NAME']
            return redirect('/index')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    print(list(request.form))
    if request.method == 'POST' and 'first_name' in request.form and 'password' in request.form and 'email_id' in request.form and 'last_name' in request.form and 'pno' in request.form and 'user_name' in request.form :
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        email_id = request.form['email_id']
        user_name = request.form['user_name']
        pno = request.form['pno']

        # print(cursor)
        sql = 'SELECT * FROM user_accounts WHERE email_id = ?'
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email_id)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account: 
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
            msg = 'Invalid email address !'
        elif not first_name or not last_name or not password or not email_id or not pno or not user_name:
            msg = 'Please fill out the form !'
        else:
            sql = 'INSERT INTO user_accounts(EMAIL_ID,FIRST_NAME,LAST_NAME,PASSWORD,PNO,USER_NAME) VALUES (?, ?, ? , ? , ? , ? )'
            stmt = ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,email_id)
            ibm_db.bind_param(stmt,2,first_name)
            ibm_db.bind_param(stmt,3,last_name)
            ibm_db.bind_param(stmt,4,password)
            ibm_db.bind_param(stmt,5,pno)
            ibm_db.bind_param(stmt,6,user_name)
            ibm_db.execute(stmt)
            session['loggedin'] = True
            session['session_id'] = hash(email_id+str(hash(password+str(time.time()))))
            session['email_id'] = email_id
            session['user_name'] = user_name
            session['first_name'] = first_name
            session['last_name'] = last_name
            msg = 'You have successfully registered !'
            return redirect('/')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/register-issue',methods=['POST'])
def registerIssue():
    if request.method == 'POST' and 'title' in request.form and 'description' in request.form:
        title = request.form['title']
        description = request.form['description']
        
        sql = 'INSERT INTO issue_db(email_id,title,description) VALUES(?,?,?)'
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1,session['email_id'])
        ibm_db.bind_param(stmt,2,title)
        ibm_db.bind_param(stmt,3,description)
        # ibm_db.bind_param(stmt,4,session['user_id'])
        ibm_db.execute(stmt)
        return 'Issue ticket created successfully'




# for admin controls-------------------------------------------------------------------

@app.route('/admin',methods=['POST','GET'])
def admin():
    sql = 'SELECT agent_id,email_id,solved_issues,pending_issues,profilepic,name FROM agent_accounts'
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    sql = 'SELECT * FROM issue_db where solved=0'
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.execute(stmt)
    issue = ibm_db.fetch_assoc(stmt)
    agents = []
    issues = []
    if(account):agents.append(account)
    if(issue):issues.append(issue)
    print(account)
    return render_template('admin.html',agents=agents,name="mohan",issues=issues)


@app.route('/new-agent-register',methods=['POST'])
def newAgentRegister():
    if 'name' in request.form and 'email_id' in request.form and 'password' in request.form:
        name = request.form['name']
        email_id = request.form['email_id']
        password = request.form['password']
        sql = 'INSERT INTO agent_accounts(name,email_id,solved_issues,pending_issues,password,profilepic) VALUES(?,?,0,0,?,?)'
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,name)
        ibm_db.bind_param(stmt,2,email_id)
        ibm_db.bind_param(stmt,3,password)
        ibm_db.bind_param(stmt,4,'http://surl.li/dljov')
        ibm_db.execute(stmt)
        return 'New Agent Created Successfully' 
    return 'Error creating new agent'
@app.route('/assign-job-to-agent',methods=['POST'])
def assignJobToAgent():
    if 'agent_id' in request.form and 'ticket' in request.form:
        agent_id = request.form['agent_id']
        ticket = request.form['ticket']
        sql = 'UPDATE issue_db SET agent_id=? WHERE ticket=?'
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,agent_id)
        ibm_db.bind_param(stmt,2,ticket)
        ibm_db.execute(stmt)
        sql = 'UPDATE AGENT_ACCOUNTS SET pending_issues = pending_issues+1 WHERE agent_id=?'
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,agent_id)
        ibm_db.execute(stmt)
        return 'New Job Assigned to agent %s',agent_id
    return 'Error Assigning Job to Agent'


#---------------For agent----------------


@app.route('/agent')
def agent_page():
    sql = 'SELECT * FROM issue_db WHERE SOLVED=0 AND AGENT_ID = 1'
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.execute(stmt)
    job_list = ibm_db.fetch_assoc(stmt)
    print(job_list)
    return render_template('agent.html',job_list=job_list)  

@app.route('/update-task', methods = ['PUT'])
def user():
    if request.method == 'PUT' and 'ticket' in request.form and 'agent_id' in request.form:
        ticket = request.form['ticket']
        agent_id = request.form['agent_id']
        sql = 'UPDATE issue_db SET solved=1 where ticket= ?'
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,ticket)
        ibm_db.execute(stmt)
        sql = 'UPDATE agent_accounts SET solved_issues=solved_issues+1 AND pending_issues=pending_issues-1 WHERE agent_id= ?'
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,agent_id)
        ibm_db.execute(stmt)
        return 'Solved Issue Ticket %s',ticket
    return 'Error Completing Job'       

@app.route('/solve-task/<ticket>')
def solveTask(ticket):
    if ticket != None:
        sql = 'SELECT * FROM issue_db WHERE ticket= ?'
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,ticket)
        ibm_db.execute(stmt)
        ticket = ibm_db.fetch_assoc(stmt)
        return render_template("agent-client-ticket.html",ticket=ticket)
    return 'Error'


# app.run(use_reloader=True)
if __name__ == '__main__':
    # from livereload import Server
    # server = Server(app.wsgi_app)
    app.run(debug=True)
    app.run()
    # server.serve(host = '0.0.0.0',port=5000)
    