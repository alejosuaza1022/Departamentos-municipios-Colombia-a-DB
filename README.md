# Departamentos-municipios-Colombia-a-DB
## Leer datos de municipios, departamentos de colombia y poder pasarlos a una DB relacional en este caso postgres
Se utilizan datos del Dane obtenidos mediante petición http y aplicar un script para generar los departamentos con sus respectivos municipios, 
para posteriormente ingresarlos a una BD postgres con tabla relacionada entre departamentos y municipios.

vale aclarar que debes crear la bd llamada como quieras y configurar en el archivo .env los datos de conexión a la BD
para las librerias se utiliza el entorno virtual pipenv, las librerias están en el arvhivo Pipfile.

links API https://geoportal.dane.gov.co/laboratorio/serviciosjson/gdivipola/servicios/municipios.php
          https://geoportal.dane.gov.co/laboratorio/serviciosjson/gdivipola/servicios/departamentos.php          
