import psycopg2
import traceback
import json
import os
from dotenv import load_dotenv
load_dotenv('.env')

data_json = {}
con = psycopg2.connect(dbname=os.getenv('DBNAME'), user=os.getenv('DBUSER'),
                       host=os.getenv('DBHOST'), password=os.getenv('DBPASS'), sslmode='require')


def generate_dep_mun():
    global data_json
    with open('departamentos.json') as json_file:
        data = json.load(json_file)
        for element in data['resultado']:
            data_json.update({
                element['CODIGO_DEPARTAMENTO']: {"Nombre": element['NOMBRE_DEPARTAMENTO'], "Municipios": []}})

    with open('Departamentos-Municipios.json', 'w', encoding='utf8')as outfile:
        json.dump(data_json, outfile, ensure_ascii=False)


def complete_dep_mun():
    global data_json
    with open('municipios.json') as json_file:
        data = json.load(json_file)
        for element in data['resultado']:
            id_dept = element['CODIGO_DEPARTAMENTO']
            data_to_fill = {
                "id": int(element['CODIGO_DPTO_MPIO']), "Nombre": element['NOMBRE_MUNICIPIO']}
            data_json.get(id_dept).get('Municipios').append(data_to_fill)
        with open('Departamentos-Municipios-lleno.json', 'w', encoding='utf8')as outfile:
            json.dump(data_json, outfile, ensure_ascii=False)


generate_dep_mun()
complete_dep_mun()


def fill_DB():
<<<<<<< HEAD
    list_fields = ('id', 'name', 'state_id')
=======
    list_fields = ('id', 'city_name', 'state_id')
>>>>>>> f4a47b22cf0a2c982779680fe27c004c945bfa9a
    with con:
        try:
            curs = con.cursor()
            query_table_states = 'create table if not exists states (id integer, name varchar, constraint pk_states PRIMARY KEY(id));'
            querry_table_cities = 'create table if not exists cities (id integer, name varchar, id_state integer, CONSTRAINT fk_citys_states FOREIGN KEY(id_state)  REFERENCES states(id) ON DELETE CASCADE);'
            curs.execute(query_table_states)
            curs.execute(querry_table_cities)
            for id, value in data_json.items():
                data_to_insert = []
                municipios = value['Municipios']
                for v in municipios:
                    v['id_depart'] = int(id)
                    data_to_insert.append(tuple(v.values()))
                nom_dep = value['Nombre']
                query = f"INSERT INTO states (id,state_name) values ({id},'{nom_dep}');"
                query1 = curs.mogrify(query + "INSERT INTO {} ({}) VALUES {}".format(
                    'cities',
                    ','.join(list_fields),
                    ','.join(['%s'] * len(municipios))
                ), data_to_insert)
                print(query1)
                curs.execute(query1)
        except Exception:
            traceback.print_exc()


fill_DB()
