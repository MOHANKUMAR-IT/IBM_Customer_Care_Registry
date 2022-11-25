from flask import Flask, render_template, request, redirect, url_for, session ,flash , Blueprint

from TCEDesk_Engine.Emailer import alertMail
from TCEDesk_Engine.DB2Queries import insertQuery,selectQuery,updateQuery,deleteQuery

import time


agent_bp = Blueprint('agent_bp', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='static')



@agent_bp.route('/')
def agent():
    if session.get("email_id"):
        jobs = selectQuery(['*'],'issue_db',['SOLVED','AGENT_ID'],[0,session.get("agent_id")])
        job_list = []
        if jobs:
            job_list = jobs   
        return render_template('agent.html',job_list=job_list) 
    else:
        return redirect('/agent/login') 

@agent_bp.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    # print("came in")
    if request.method == 'POST' and 'email_id' in request.form and 'password' in request.form:
        # print(request.form)
        email_id = request.form['email_id']
        password = request.form['password']
        print(email_id,password)

        account = selectQuery(['*'],'agent_accounts',['EMAIL_ID','PASSWORD'],[email_id,password])

        if account:
            account = account[0]
            session['loggedin'] = True
            session['agent_id'] = account['AGENT_ID']
            session['session_id'] = hash(account['EMAIL_ID']+str(hash(account['PASSWORD']+str(time.time()))))
            session['email_id'] = email_id
            session['name'] = account['NAME']
            session['type'] = 'AGENT_ACCOUNTS'
            session['first_name']=account['FIRST_NAME']
            session['last_name']=account['LAST_NAME']   
            session['pno'] = account["PNO"]
            session['profile'] = account["PROFILE"]
            session['location']=account["LOCATION"]
            session['password']=account['PASSWORD']
            session['agent_id'] = account['AGENT_ID']
            session['solved_issues'] = account['SOLVED_ISSUES']
            session['pending_issues'] = account['PENDING_ISSUES']
            return redirect('/agent')
        else:
            msg = 'Incorrect username / password !'
    return render_template('agent-login.html', msg = msg)

@agent_bp.route('/update-task', methods = ['PUT'])
def updateTask():
    if request.method == 'PUT' and 'ticket' in request.form and 'agent_id' in request.form:
        ticket = request.form['ticket']
        agent_id = request.form['agent_id']
        updateQuery('UPDATE issue_db SET solved=1 where ticket= ?',[ticket])
        updateQuery('UPDATE agent_accounts SET solved_issues=solved_issues+1 , pending_issues=pending_issues-1 WHERE agent_id= ?',[agent_id])
        flash('Solved Issue Ticket %s',ticket)
        return redirect(request.url)
    flash('Error Completing Job')  
    return redirect('/agent')   

@agent_bp.route('/solve-task/<ticket>')
def solveTask(ticket):
    if ticket != None:

        ticket = selectQuery(['*'],'issue_db',['ticket'],[ticket])
        return render_template("agent-client-ticket.html",ticket=ticket)
    flash('Error')
    return redirect('/agent/solve-task/'+ticket)

@agent_bp.route('/update-progress',methods=["POST"])
def update_progress():
    updateQuery('UPDATE issue_db SET progress=? WHERE ticket=?',[request.form['progress'],request.form['ticket']])
    flash("Applied changes")
    return redirect('/agent/solve-task/'+request.form['ticket'])

@agent_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

