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



if __name__ == '__main__':
    app.run(debug=True)
    app.run()

    