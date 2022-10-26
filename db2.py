from sqlite3 import connect
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fgp33793;PWD=DXgCxphsnaCXNucS",'','')

# DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;UID=fgp33793;PWD=DXgCxphsnaCXNucS

# sql = "INSERT INTO user_accounts(email_id,first_name,last_name,password,pno) VALUES(?,?,?,?,?)"
# sql = "DELETE FROM ISSUE_DB"
sql = 'SELECT * FROM ISSUE_DB FETCH FIRST 2 ROWS ONLY' 
# stmt = ibm_db.prepare(conn,sql)
# ibm_db.bind_param(stmt,1,'mohankumar@student.tce.edu')
# ibm_db.bind_param(stmt,2,password)
# ibm_db.execute(stmt)
# account = ibm_db.fetch_assoc(stmt)

# ibm_db.bind_param(stmt,1,"mohankumar@student.tce.edu")
# ibm_db.bind_param(stmt,2,"Mohan")
# ibm_db.bind_param(stmt,3,"Kumar")
# ibm_db.bind_param(stmt,4,"StrongPixel1090")
# ibm_db.bind_param(stmt,5,"7010969868")
# sql = 'SELECT * FROM agent_accounts'
stmt = ibm_db.prepare(conn,sql)
ibm_db.execute(stmt)
account = ibm_db.fetch_tuple(stmt)
print(account)  

