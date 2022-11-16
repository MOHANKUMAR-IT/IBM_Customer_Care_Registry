from flask import Flask, render_template, request, redirect, url_for, session ,flash,Blueprint

from TCEDesk_Engine.Emailer import alertMail
from TCEDesk_Engine.DB2Queries import insertQuery,selectQuery,updateQuery,deleteQuery

import time
import re

user_bp = Blueprint('user_bp', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='static')


@user_bp.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

    
@user_bp.route('/')    
def landing_page():
    if session.get("email_id"):
        pending_issue_data = []
        data = selectQuery(['ticket','title','agent_id','progress'],'issue_db',['email_id','solved'],[session['email_id'],0])
        pending_issue_headings = []
        solved_issue_data = []
        if data:
            pending_issue_data.append(data)
            pending_issue_headings = data.keys()

        data = selectQuery(['ticket','title','agent_id'],'issue_db',['email_id','solved'],[session['email_id'],1])
        solved_issue_headings = []
        if data:
            solved_issue_data.append(data)
            solved_issue_headings = data.keys()
        print(pending_issue_data)
        return render_template("index.html",pending_issue_data=pending_issue_data,pending_issue_headings=pending_issue_headings,solved_issue_headings=solved_issue_headings,solved_issue_data=solved_issue_data)
    else:
        return render_template('login.html')


@user_bp.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email_id' in request.form and 'password' in request.form:

        email_id = request.form['email_id']
        password = request.form['password']
        print(email_id,password)

        account = selectQuery(['*'],'user_accounts',['email_id','password'],[email_id,password])

        if account:
            session['loggedin'] = True
            session['session_id'] = hash(account['EMAIL_ID']+str(hash(account['PASSWORD']+str(time.time()))))
            session['email_id'] = email_id
            session['user_name'] = account['USER_NAME']
            session['password']=account['PASSWORD']
            session['location']=account["LOCATION"]
            session['profile']=account["PROFILE"]
            session['dob']=account['DATE_OF_BIRTH']
            session['pno'] = account['PNO']
            session['type'] = 'USER_ACCOUNTS'
            session['first_name'] = account['FIRST_NAME']
            session['last_name'] = account['LAST_NAME']
            session['user_id'] = account['USER_ID']
            return redirect('/user')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)



@user_bp.route('/register', methods =['GET', 'POST'])
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

        account = selectQuery(['*'],'user_accounts',['email_id'],[email_id])
        
        if account: 
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
            msg = 'Invalid email address !'
        elif not first_name or not last_name or not password or not email_id or not pno or not user_name:
            msg = 'Please fill out the form !'
        else:
            insertQuery(['EMAIL_ID', 'FIRST_NAME', 'LAST_NAME', 'PASSWORD', 'PNO', 'USER_NAME', 'PROFILE'],'user_accounts',[email_id,first_name,last_name,password,pno,user_name,"/user/static/man.png"])
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
            msg = 'You have successfully registered !'
            return redirect('/user')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@user_bp.route('/register-issue',methods=['POST'])
def registerIssue():
    if request.method == 'POST' and 'title' in request.form and 'description' in request.form:
        title = request.form['title']
        description = request.form['description']
        
        insertQuery(['email_id', 'title', 'description', 'user_id'],'issue_db',[session['email_id'],title,description,session['user_id']])

        content = "<h1>Your issue has been taken into account <br> Ticket => <br> Title: "+title+" <br> Description: "+description+" <br><br> An agent will be alloted to solve your issue.<br>Thanks and Regards,<br><i>Team TCE-Desk</i>"
        alertMail(session['email_id'],"TCE Desk Issue Ticket",content)
        flash('Issue ticket created successfully')
        return redirect('/user')


