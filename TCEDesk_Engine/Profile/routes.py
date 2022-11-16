from flask import Flask, render_template, request, redirect, url_for, session ,flash,Blueprint

from werkzeug.utils import secure_filename

from TCEDesk_Engine.DB2Queries import updateQuery

from dotenv import load_dotenv 

import os

load_dotenv()

profile_bp = Blueprint('profile_bp', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='static')


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.path.join(basedir, 'static/profile')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    

@profile_bp.route('/',methods=["GET","POST"])
def profile():
    if session.get("email_id"):
        if request.form:
            type = session['type']
            id = ""
            if type=="AGENT_ACCOUNTS":
                id = "agent_id"
            else:
                id = "user_id"
            updateQuery('UPDATE '+type+' SET user_name= ?,first_name= ?,last_name= ?,pno= ?,password= ?,email_id= ?,location= ?,date_of_birth= ? WHERE '+id+'= ?',[request.form["name"],\
                request.form["first_name"],request.form['last_name'],request.form['pno'],request.form['password'],request.form['email_id'],request.form['location'],request.form['dob'],\
                session[id] ])

            for i in request.form:
                session[i] = request.form[i]

            print("\n\nUPDATE PROFILE for "+request.form['name']+" --------------------------------------------------\n\n")
        return render_template('profile.html')
    else:
        return redirect('/')

@profile_bp.route('/profile-img',methods=['POST'])
def profile_img():
    file = request.files['profile']
    if file.filename == '':
        flash('No file was selected')
        return redirect(request.url)
    elif file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        filename=str(session['user_id'] if (session['type']=="USER_ACCOUNTS") else session['agent_id'])
        filename = filename+'.'+secure_filename(file.filename).rsplit('.', 1)[1].lower()
        file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
        flash('Image has been successfully uploaded')
        session['profile'] = '/static/profilepic/'+filename

        updateQuery('UPDATE '+session['type']+' SET profile = ? WHERE user_id= ?',[session['profile'],session['user_id'] if (session['type']=="USER_ACCOUNTS") else session['agent_id']])

        return redirect('/profile')
    else:
        flash('Allowed media types are - png, jpg, jpeg, gif')
        return redirect(request.url)

