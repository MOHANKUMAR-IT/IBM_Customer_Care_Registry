import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fgp33793;PWD=DXgCxphsnaCXNucS",'','')

def selectQuery(columns,table,conditions=None,conditionValues=None):
    
    sql = 'SELECT '

    for i in range(len(columns)):
        sql+=columns[i]
        if(i+1!=len(columns)):
            sql+=', '
    
    sql+=' FROM '+table+' '
    if conditions:
        sql+=' WHERE '
        for i in range(len(conditions)):
            sql+=conditions[i]+'=? '
            if(i+1!=len(conditions)):
                sql+='AND '
    
    stmt = ibm_db.prepare(conn,sql)
    # print(sql)
    if conditionValues:
        for i in range(len(conditionValues)):
            ibm_db.bind_param(stmt,i+1,conditionValues[i])
    
    ibm_db.execute(stmt)
    data = ibm_db.fetch_assoc(stmt)

    return data
    

def insertQuery(columns,table,values):
    sql = 'INSERT INTO '+table
    if columns:
        sql+='('
        for i in range(len(columns)):
            sql+=columns[i]
            if i!=len(columns)-1:
                sql+=','
        sql+=') '
    if values:
        sql+=' VALUES('
        for i in range(len(values)):
            sql+=' ? '
            if i!=len(values)-1:
                sql+=','
    sql+=')'
    stmt = ibm_db.prepare(conn,sql)
    # print(sql)
    for i in range(len(values)):
        ibm_db.bind_param(stmt,i+1,values[i])
    print(sql)
    ibm_db.execute(stmt)

def updateQuery(sql,values):
    stmt = ibm_db.prepare(conn,sql)
    for i in range(len(values)):
        ibm_db.bind_param(stmt,i+1,values[i])
    ibm_db.execute(stmt)
    
def deleteQuery(sql,values):
    stmt = ibm_db.prepare(conn,sql)
    for i in range(len(values)):
        ibm_db.bind_param(stmt,i+1,values[i])
    ibm_db.execute(stmt)
