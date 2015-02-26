import config
import mysql.connector
from mysql.connector import errorcode
import datetime

try:
    cnx = mysql.connector.connect(user=config.mysql['user'], password=config.mysql['password'],
                                  host='localhost',
                                  database='alumbrado')
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exists")
    else:
        print(err)
    exit(0)

fallas_query = ("SELECT fault_id, error_key, asset_external_id, creation_timestamp FROM fallas")
try:
    cursor.execute(fallas_query)
except:
    print("No se pudo ejecutar query")

fallas = cursor.fetchall()
cnx.commit()
cursor.close()

for falla in fallas:
    fault_id = falla[0]    
    error_key = falla[1]
    asset_external_id = falla[2]
    creation_timestamp = falla[3]
    hora_ahora = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:00:00')

    exists_query = ("SELECT COUNT(1) FROM luminarias_delta WHERE fault_id = '%s'")
    cursor = cnx.cursor()
    
    try:
        cursor.execute(exists_query, (fault_id))
    except:
        print "No se pudo ejecutar query"
    
    count = cursor.fetchall()
    cnx.commit()
    cursor.close()
    
    if (count[0][0] == 0):        
        cursor = cnx.cursor()

        insert_query = ("INSERT INTO luminarias_delta "
                        "(fault_id, asset_external_id, fecha_recorded, tipo_falla, is_working, last_updated) "
                        "VALUES ('%s', %s, %s, %s, %s, %s)")
        try:
            cursor.execute(insert_query, (fault_id, asset_external_id, hora_ahora, error_key, 0, creation_timestamp))
        except:
            print("No se pudo agregar falla " + str(fault_id))

        cnx.commit()
        cursor.close()

cnx.close()
