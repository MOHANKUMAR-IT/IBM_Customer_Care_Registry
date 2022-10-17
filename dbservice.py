

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import time
import json


app = Flask(__name__)

app.secret_key = 'StrongPixel1090!'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'customer_care_registry'

mysql = MySQL(app)

@app.route('/')
def landing_page():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM issue_db WHERE solved=0 AND agent_id LIKE %s',(1,))
    job_list = cursor.fetchall()
    # print(job_list)
    return render_template('agent.html',job_list=job_list)  

@app.route('/update-task', methods = ['PUT'])
def user():
    if request.method == 'PUT' and 'ticket' in request.form and 'agent_id' in request.form:
        ticket = request.form['ticket']
        agent_id = request.form['agent_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE issue_db SET solved=1 where ticket=%s',(ticket,))
        cursor.execute('UPDATE agent_accounts SET solved_issues=solved_issues+1 AND pending_issues=pending_issues-1 WHERE agent_id=%s',(agent_id,))
        mysql.connection.commit()
        return 'Solved Issue Ticket %s',ticket
    return 'Error Completing Job'       

@app.route('/solve-task/<ticket>')
def solveTask(ticket):
    if ticket != None:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM issue_db WHERE ticket=%s',(ticket,))
        job = cursor.fetchone() 
        return render_template("agent-client-ticket.html",ticket=ticket)
    return 'Error'

if __name__ == '__main__':

    app.run(debug=True)
    app.run()

    