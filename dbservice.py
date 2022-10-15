from os import access
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
def landing_page():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT agent_id,email_id,solved_issues,pending_issues,profilepic,name FROM agent_accounts')
    account = cursor.fetchall()
    print(account[0])
    return render_template('admin.html',agents=account,name="mohan")

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
# app.run(use_reloader=True)
if __name__ == '__main__':
    # from livereload import Server
    # server = Server(app.wsgi_app)
    app.run(debug=True)
    app.run()
    # server.serve(host = '0.0.0.0',port=5000)
    