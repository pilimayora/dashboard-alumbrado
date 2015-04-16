# Dashboard Alumbrado

### Información periódica del estado de las luminarias de la ciudad

En este proyecto se encuentras los scripts que actualizan periódicamente una base de datos con la información de luminarias.

## Requerimientos técnicos

* Python 2.7+
  * Módulos de Python:
  	* mysql-connector-python
  	* suds-jurko
  	* xlrd
* MySQL
* phpMyAdmin (opcional pero recomendado para comodidad del usuario)

## Pasos a seguir para correr los scripts

1. Modificar el archivo config.py con los valores correspondientes
2. Agregar cron jobs para correr los diferentes scripts. La frecuencia la debe definir el cliente.