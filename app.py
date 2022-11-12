from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
import time
from myemail import alertMail

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
            session['user_id'] = account['USER_ID']
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
            content = '''
                <div style="background-image:url('https://images.unsplash.com/photo-1664689708549-18f26a776256?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80');
                        height:600px;
                        width:100%;
                        background-repeat:no-repeat;
                        opacity:1;">
                        <p style="
                        box-shadow:0 0 0 2px white;
                        text-shadow: 3px 3px black;
                        position:absolute;
                        font-size: 60px;
                        z-index:2;
                        text-align:center;
                        color:white;">Congratulations '''+user_name+''',<br>You have successfully registered new account with us...<p>
                </div>
            '''
            alertMail(email_id,"TCE Desk User Registration",content)
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
        
        sql = 'INSERT INTO issue_db(email_id,title,description,user_id) VALUES(?,?,?,?)'
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, session['email_id'])
        ibm_db.bind_param(stmt, 2, title)
        ibm_db.bind_param(stmt, 3, description)
        ibm_db.bind_param(stmt, 4, session['user_id'])
        ibm_db.execute(stmt)
        content = "<h1>Your issue has been taken into account <br> Ticket => <br> Title: "+title+" <br> Description: "+description+" <br><br> An agent will be alloted to solve your issue.<br>Thanks and Regards,<br><i>Team TCE-Desk</i>"
        alertMail(session['email_id'],"TCE Desk Issue Ticket",content)
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
    if(isinstance(account,dict)):agents.append(account)
    else: agents=account
    if(isinstance(issue,dict)):issues.append(issue)
    else:issues=issue
    print(issues,len(issues))
    print(agents,len(agents))
    return render_template('admin1.html',agents=agents,name="mohan",issues=issues)


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
        content=f"<h1>Hi {name},<br>We are happy to inform you that you are a part of TCE Desk.<br>Account details,<br>Email Id: {email_id}<br>Password: {password}<br><br>Keep your credentials safer and dont disclose it.<br>Thanks and Regards,<br><i>Team TCE-Desk</i>"
        alertMail(session['email_id'],"TCE Desk Careers",content)
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

        sql = 'SELECT * FROM issue_db WHERE ticket=?'
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,ticket)
        ibm_db.execute(stmt)
        issue = ibm_db.fetch_assoc(stmt)
        content="<h1>Hi Agent,<br>You have been assigned a task to solve Issue details=><br>Ticket:{}<br>Title:{} <br>Description: {} <br>User Email Id: {}<br>For further information contact user through his mail id.<br>Thanks and Regards,<br><i>Team TCE-Desk</i>".format(issue['TICKET'],issue['TITLE'],issue['DESCRIPTION'],issue['EMAIL_ID'])
        alertMail(session['email_id'],"TCE Desk Tasks",content)
        alertMail(issue['EMAIL_ID'],"TCE Desk Agent Allotted","<h1>Dear User,Your Iussue with ticket:{} has been alloted Agent:{} .Issue will be cleared soon enough<br><br>Thanks and Regards,<br><i>Team TCE-Desk</i>".format(issue['TICKET'],issue['AGENT_ID']))
        return 'New Job Assigned to agent '+str(agent_id)
        
    return 'Error Assigning Job to Agent'

#---------------For agent----------------

@app.route('/agent')
def agent():
    if session.get("email_id"):
        sql = 'SELECT * FROM issue_db WHERE SOLVED=0 AND AGENT_ID = ?'
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,session.get("agent_id"))
        ibm_db.execute(stmt)
        jobs = ibm_db.fetch_assoc(stmt)
        job_list = []
        print(jobs)
        if jobs:
            job_list.append(jobs)   
        return render_template('agent.html',job_list=job_list) 
    else:
        return redirect('agent_login') 

@app.route('/agent_login', methods =['GET', 'POST'])
def agent_login():
    msg = ''
    # print("came in")
    if request.method == 'POST' and 'email_id' in request.form and 'password' in request.form:
        # print(request.form)
        email_id = request.form['email_id']
        password = request.form['password']
        print(email_id,password)
        sql = 'SELECT * FROM agent_accounts WHERE EMAIL_ID = ? AND PASSWORD = ?'

        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email_id)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            session['loggedin'] = True
            session['session_id'] = hash(account['EMAIL_ID']+str(hash(account['PASSWORD']+str(time.time()))))
            session['email_id'] = email_id
            session['name'] = account['NAME']
            session['agent_id'] = account['AGENT_ID']
            session['solved_issues'] = account['SOLVED_ISSUES']
            session['pending_issues'] = account['PENDING_ISSUES']
            return redirect(url_for('agent'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('agent-login.html', msg = msg)

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

@app.route('/update-progress',methods=["POST"])
def update_progress():
    sql = 'UPDATE issue_db SET progress=? WHERE ticket=?'
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,request.form['progress'])
    ibm_db.bind_param(stmt,2,request.form['ticket'])    
    ibm_db.execute(stmt)
    return "Applied changes"


if __name__ == '__main__':
    # from livereload import Server
    # server = Server(app.wsgi_app)
    app.run(debug=True)
    app.run(use_reloader=True)
    # app.run()
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)
    # server.serve(host = '0.0.0.0',port=5000)
    