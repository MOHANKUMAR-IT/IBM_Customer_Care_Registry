from flask import Flask, render_template, request, redirect, url_for, session ,flash,Blueprint

from TCEDesk_Engine.Emailer import alertMail
from TCEDesk_Engine.DB2Queries import insertQuery,selectQuery,updateQuery,deleteQuery
import ibm_db

admin_bp = Blueprint('admin_bp',__name__,static_folder='static',static_url_path='static',template_folder='templates')

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fgp33793;PWD=DXgCxphsnaCXNucS",'','')


@admin_bp.route('/',methods=['POST','GET'])
def admin():
    if session.get("loggedin"):
        account = selectQuery(['*'],'agent_accounts')
        issue = selectQuery(['*'],'issue_db',['solved'],[0])
        agents = []
        issues = []
        agents =account
        issues = issue
        print(agents)
        return render_template('admin.html',agents=agents,issues=issues)
    else:
        return redirect('/admin/admin-login')
@admin_bp.route('/admin-login',methods=['POST','GET'])
def admin_login():
    msg = ''
    print(dict(request.form))
    if 'password' in request.form:
        if(request.form['password']=='admin'):
            session['loggedin'] = True
            return redirect('/admin')
        msg = 'Incorrect password!'

    return render_template('admin-login.html',msg=msg)


@admin_bp.route('/new-agent-register',methods=['POST'])
def newAgentRegister():
    if 'name' in request.form and 'email_id' in request.form and 'password' in request.form:
        name = request.form['name']
        email_id = request.form['email_id']
        password = request.form['password']
    
        insertQuery(['name', 'email_id', 'solved_issues', 'pending_issues', 'password', 'profile'],'agent_accounts',[name,email_id,0,0,password,'http://surl.li/dljov'])

        content=f"<h1>Hi {name},<br>We are happy to inform you that you are a part of TCE Desk.<br>Account details,<br>Email Id: {email_id}<br>Password: {password}<br><br>Keep your credentials safer and dont disclose it.<br>Thanks and Regards,<br><i>Team TCE-Desk</i>"
        alertMail(email_id,"TCE Desk Careers",content)

        flash('New Agent Created Successfully')
        return redirect('/admin')
    flash('Error creating new agent')
    return redirect('/admin')

@admin_bp.route('/assign-job-to-agent',methods=['POST'])
def assignJobToAgent():
    if 'agent_id' in request.form and 'ticket' in request.form:
        
        agent_id = request.form['agent_id']
        ticket = request.form['ticket']
        print("Agent Id",agent_id)

        updateQuery('UPDATE issue_db SET agent_id=? WHERE ticket=?',[agent_id,ticket])  

        updateQuery('UPDATE AGENT_ACCOUNTS SET pending_issues = pending_issues+1 WHERE agent_id=?',[agent_id])
        agentAcc = selectQuery(['email_id'],'agent_accounts',['agent_id'],[agent_id])
        issue = selectQuery(['*'],'issue_db',['ticket'],[ticket])
    
        content="<h1>Hi Agent,<br>You have been assigned a task to solve Issue details=><br>Ticket:{}<br>Title:{} <br>Description: {} <br>User Email Id: {}<br>For further information contact user through his mail id.<br>Thanks and Regards,<br><i>Team TCE-Desk</i>".format(issue['TICKET'],issue['TITLE'],issue['DESCRIPTION'],issue['EMAIL_ID'])
        alertMail(agentAcc,"TCE Desk Tasks",content)
        alertMail(issue['EMAIL_ID'],"TCE Desk Agent Allotted","<h1>Dear User,Your Iussue with ticket:{} has been alloted Agent:{} .Issue will be cleared soon enough<br><br>Thanks and Regards,<br><i>Team TCE-Desk</i>".format(issue['TICKET'],issue['AGENT_ID']))
        flash('New Job Assigned to agent '+str(agent_id))
        return redirect('/admin')
        
    flash('Error Assigning Job to Agent')
    return redirect('/admin')

@admin_bp.route('/removeAgent',methods=['POST'])
def removeAgent():
    print("\n\n\n\nremoving agent\n\n\n")
    if 'agent_id' in request.form:
        agent_id = request.form['agent_id']
        updateQuery('UPDATE issue_db SET agent_id=0 WHERE agent_id=?',[agent_id])
        
        deleteQuery('DELETE FROM agent_accounts WHERE agent_id=?',[agent_id])
        agentAcc = selectQuery(['email_id'],'agent_accounts',['agent_id'],[agent_id])
        content="<h1>Hi Agent,<br>Thank your for your service with us. We wish you a very good future ahead :) .<br>Thanks and Regards,<br><i>Team TCE-Desk</i>"
        alertMail(agentAcc,"TCE Desk Career",content)
        return "Agent removed successfully :)"

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')