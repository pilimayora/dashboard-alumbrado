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

select_fallas = "SELECT COUNT(*) FROM fallas"

try:
    cursor1.execute(select_fallas)
except:
    print("No se pudo actualizar a los gabinetes")

fallas_count = cursor1.fetchall()[0][0]
cnx.commit()

hora_ahora = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:00:00')

# Fijarse si ya hay un conteo para esa hora
exists_query = "SELECT * FROM fallas_historico WHERE fecha = '%s'" % (hora_ahora)

try:
    cursor2.execute(exists_query)
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))

cnx.commit()

if (cursor2.rowcount == 0):        
    insert_query = ("INSERT INTO fallas_historico " 
                   "(fecha, fallas_count) " 
                   "VALUES ('%s', %s)") % (hora_ahora, fallas_count)
    try:
        cursor3.execute(insert_query)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    cnx.commit()        

cursor1.close()
cursor2.close()
cursor3.close()
cnx.close()
