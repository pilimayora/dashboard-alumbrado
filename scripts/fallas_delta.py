import config
import mysql.connector
from mysql.connector import errorcode
import datetime

try:
    cnx = mysql.connector.connect(user=config.mysql['user'], password=config.mysql['password'],
                                  host=config.mysql['host'],
                                  database='alumbrado')
    cursor1 = cnx.cursor()
    cursor2 = cnx.cursor(buffered=True)
    cursor3 = cnx.cursor()    
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exists")
    else:
        print(err)
    exit(0)

fallas_query = ("SELECT fault_id, category_key, error_key, severity, asset_external_id, creation_timestamp " 
                "FROM fallas")
try:
    cursor1.execute(fallas_query)
except:
    print("No se pudo ejecutar query")

fallas = cursor1.fetchall()
cnx.commit()

# Primero hacer el insert de todas las fallas nuevas
for falla in fallas:
    fault_id = falla[0]
    category_key = falla[1]    
    error_key = falla[2]
    severity = falla[3]
    asset_external_id = falla[4]
    creation_timestamp = falla[5]
    last_updated = creation_timestamp
    hora_ahora = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:00:00')

    exists_query = "SELECT * FROM fallas_delta WHERE fault_id = %s" % (fault_id)

    try:
        cursor2.execute(exists_query)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    
    cnx.commit()

    if (cursor2.rowcount == 0):        
        insert_query = ("INSERT INTO fallas_delta " 
                       "(fault_id, asset_external_id, fecha_recorded, last_updated, creation_timestamp, error_key, category_key, severity, is_active, duracion) " 
                       "VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s)") % (fault_id, asset_external_id, hora_ahora, last_updated, creation_timestamp, error_key, category_key, severity, 1, 0)
        try:
            cursor3.execute(insert_query)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

        cnx.commit()        

cursor1.close()
cursor2.close()
cursor3.close()

# Ahora seleccionar las fallas activas de fallas_delta, y si no estan dentro de las
# fallas del WS, cambiar el estado de activa a NO ACTIVA.
cursor4 = cnx.cursor()
cursor5 = cnx.cursor(buffered=True)
cursor6 = cnx.cursor()

fallas_activas_query = "SELECT * FROM fallas_delta WHERE is_active = 1"

try:
    cursor4.execute(fallas_activas_query)
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))

fallas_activas = cursor4.fetchall()
cnx.commit()

for falla_activa in fallas_activas:
    fault_id = falla_activa[0]
    hora_ahora = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:00:00')

    exists_query = "SELECT * FROM fallas WHERE fault_id = %s" % (fault_id)

    try:
        cursor5.execute(exists_query)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    
    cnx.commit()

    if (cursor5.rowcount == 0):        
        update_query = ("UPDATE fallas_delta SET is_active = 0, last_updated = '%s' "
                        "WHERE fault_id = %s") % (hora_ahora, fault_id)
        try:
            cursor6.execute(update_query)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

        cnx.commit() 

cursor4.close()
cursor5.close()
cursor6.close()

cnx.close()
