import os
from dotenv import load_dotenv
load_dotenv('.env')

import json
import traceback
import psycopg2
data_json = {}
con = psycopg2.connect(dbname=os.getenv('DBNAME'), user=os.getenv('USER'),
                       host=os.getenv('DBHOST'), password=os.getenv('DBPASS'))


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
    list_fields = ('id', 'name', 'state_id')
    with con:
        try:
            curs = con.cursor()
            for id, value in data_json.items():
                data_to_insert = []
                municipios = value['Municipios']
                for v in municipios:
                    v['id_depart'] =  int(id)
                    data_to_insert.append(tuple(v.values()))
                nom_dep = value['Nombre']
                query = f"INSERT INTO states (id,name) values ({id},'{nom_dep}');"
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
