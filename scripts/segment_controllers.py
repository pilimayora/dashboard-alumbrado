import config
import mysql.connector
from mysql.connector import errorcode
import datetime

try:
    cnx = mysql.connector.connect(user=config.mysql['user'], password=config.mysql['password'],
                                  host='localhost',
                                  database='alumbrado')
    cursor1 = cnx.cursor()
    cursor2 = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exists")
    else:
        print(err)
    exit(0)

update_gab_query = "UPDATE luminarias SET es_gabinete = 1 WHERE `asset_name` LIKE '%CAB-%'"

try:
    cursor1.execute(update_gab_query)
    cnx.commit()
except:
    print("No se pudo actualizar a los gabinetes")

update_mantelectric = "UPDATE luminarias SET maintainer = 'Mantelectric Zona 1' where (maintainer = 'NULL' OR maintainer = '-' OR maintainer = 'Sin_mantenedor' OR maintainer = '0000') and asset_name like 'M/%'"
update_sutec = "UPDATE luminarias SET maintainer = 'Sutec Zona 6' where (maintainer = 'NULL' OR maintainer = '-' OR maintainer = 'Sin_mantenedor' OR maintainer = '0000') and asset_name like 'S/%'"
update_lesko = "UPDATE luminarias SET maintainer = 'Lesko Zona 4' where (maintainer = 'NULL' OR maintainer = '-' OR maintainer = 'Sin_mantenedor' OR maintainer = '0000') and asset_name like 'L/%'"
update_autotrol = "UPDATE luminarias SET maintainer = 'Autotrol Construman UTE Zona 3' where (maintainer = 'NULL' OR maintainer = '-' OR maintainer = 'Sin_mantenedor' OR maintainer = '0000') and asset_name like 'A/%'"
update_ilubaires = "UPDATE luminarias SET maintainer = 'Ilubaires Zona 5' where (maintainer = 'NULL' OR maintainer = '-' OR maintainer = 'Sin_mantenedor' OR maintainer = '0000') and asset_name like 'I/%'"

try:
    cursor2.execute(update_mantelectric)
    cnx.commit()
    cursor2.execute(update_sutec)
    cnx.commit()
    cursor2.execute(update_lesko)
    cnx.commit()
    cursor2.execute(update_autotrol)
    cnx.commit()
    cursor2.execute(update_ilubaires)
    cnx.commit()
except:
    print("No se pudo actualizar a los mantenedores")

cursor1.close()
cursor2.close
cnx.close()
