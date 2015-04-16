import xlrd
import csv
import config_inventario
import mysql.connector
from mysql.connector import errorcode
import datetime

############# 
### Convertir archivo de Excel en CSV 
### Sin las primeras filas que vienen de CityTouch
#############

inv_csv = open('eventos.csv', 'wb')
inv_writer = csv.writer(inv_csv, delimiter=',')

workbook = xlrd.open_workbook('eventos.xls')
worksheet = workbook.sheet_by_name('Sheet1')

num_rows = worksheet.nrows - 1 
num_cells = worksheet.ncols - 1
curr_row = 4

while curr_row < num_rows:
	curr_row += 1
	row = worksheet.row(curr_row)
	valores_row = []
	curr_cell = -1
	while curr_cell < num_cells:
		curr_cell += 1
		cell_value = worksheet.cell_value(curr_row, curr_cell)
		cell_type = worksheet.cell_type(curr_row, curr_cell)
		# Date
		if cell_type == 3:
			cell_value = datetime.datetime(*xlrd.xldate_as_tuple(cell_value,
                                                  workbook.datemode))
		# Text to Boolean
		if cell_type == 1:
			if cell_value == "True":
				cell_value = 1
			if cell_value == "False":
				cell_value = 0
		valores_row.append(cell_value)
	inv_writer.writerow([unicode(s).encode("utf-8") for s in valores_row])

#############
### Subir inventario a tabla de MySQL
#############

# Conectarse a MySQL
try:
    cnx = mysql.connector.connect(user=config_inventario.mysql['user'], password=config_inventario.mysql['password'],
                                  host=config_inventario.mysql['host'],
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

truncate_query = "TRUNCATE TABLE eventos"

try:
    cursor1.execute(truncate_query)
    cnx.commit()
except:
    print("No se pudo trunquetear la tabla de eventos")

load_data_query = ("LOAD DATA LOCAL INFILE 'eventos.csv' "
				   "INTO TABLE eventos "
				   "FIELDS TERMINATED BY ',' "
				   "LINES TERMINATED BY '\n' "
				   "IGNORE 1 LINES ")

try:
	cursor2.execute(load_data_query)
	cnx.commit()
except mysql.connector.Error as err:
	print err

# Cerramos todo
cursor1.close()
cursor2.close()
cnx.close()