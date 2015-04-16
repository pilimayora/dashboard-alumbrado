from suds.client import Client
import config
import mysql.connector
from mysql.connector import errorcode

try:
    cnx = mysql.connector.connect(user=config.mysql['user'], password=config.mysql['password'],
                                  host=config.mysql['host'],
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

url = config.philips['wsdl_url']
public = config.philips['public_key']
private = config.philips['private_key']

client = Client(url, username=public, password=private)

# GetFaults desde la ultima revision
result = client.service.GetFaults(0)
fault_items = result.FaultItems

if (fault_items is not None):
    # Truncate tabla de fallas
    truncate_query = ("TRUNCATE TABLE fallas")
    try:
        cursor.execute(truncate_query)
    except:
        print("No se pudo vaciar la tabla de fallas")

    for fault_item in fault_items:
        for fault in fault_item[1]:        
            fault_id = int(fault.FaultId)
            category_key = str(fault.CategoryKey)
            error_key = str(fault.ErrorKey)
            severity = str(fault.Severity)
            asset_external_id = str(fault.AssetExternalId)
            creation_timestamp = str(fault.CreationTimestamp)  
            insert_query = ("INSERT INTO fallas "
                            "(fault_id, category_key, error_key, severity, asset_external_id, creation_timestamp) "
                            "VALUES ('%s', %s, %s, %s, %s, %s)")
            try:
                cursor.execute(insert_query, (fault_id, category_key, error_key, severity, asset_external_id, creation_timestamp))
                cnx.commit()
            except:
                print("No se pudo agregar falla " + str(fault_id))

cursor.close()
cnx.close()
