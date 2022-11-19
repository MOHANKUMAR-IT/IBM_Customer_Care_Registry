import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fgp33793;PWD=DXgCxphsnaCXNucS",'','')


sql = 'SELECT * FROM USER_ACCOUNTS'
stmt = ibm_db.prepare(conn,sql)
ibm_db.execute(stmt)
# data = ibm_db.fetch_tuple(stmt)
# print(data)
data = []
dictionary = ibm_db.fetch_assoc(stmt)
while dictionary != False:
    data.append(dict(dictionary))
    # print("The ID is : ", dictionary["AGENT_ID"])
    dictionary = ibm_db.fetch_assoc(stmt)
print(data)