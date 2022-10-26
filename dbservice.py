from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
import time
import json
from flask_session import Session

app = Flask(__name__)

app.config['SECRET_KEY'] = "StrongPixel1090"
app.config['SESSION_TYPE'] = 'filesystem'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fgp33793;PWD=DXgCxphsnaCXNucS",'','')
Session(app)


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

if __name__ == '__main__':
    app.run(debug=True)
    app.run()

    