from flask import Flask, request, render_template   #request sem s
import MySQLdb
import requests
import json
import pandas as pd


app = Flask(__name__)

conn = MySQLdb.connect(host="localhost", user="root", db="test" )
conn.autocommit(True)
cursor=conn.cursor()

@app.route("/", methods=["GET"]) #se eu colocar assim,vai usar a mesma rota do endereço padrão
def index():
    return "Hello Alô Hola!!!!"


@app.route("/cadastrar/", methods = ["POST"])
def cadastrar():
    raw_request = request.data.decode("utf-8")
    dict_values = json.loads(raw_request)
    try:
        sql = "INSERT INTO test_table (Name, Idade, Animal) VALUES " \
              f"('{dict_values['Name']}', {dict_values['Idade']}, {dict_values['Animal']})"

        affected_rows = cursor.execute(sql)
        if affected_rows > 0:
            return "Deu tudo certo!", 200
    except Exception as error:
        return str(error.args)
    return "Algo deu errado!", 400



@app.route("/deletar/<int:id>", methods=["DELETE"])
def delete(id):
    cursor.execute(f"DELETE FROM test_table WHERE id = {id}")
    return "Apagado com sucesso!"


@app.route("/read/")
@app.route("/read/<int:id>")
def read(id=None):
    sql = "SELECT * FROM test_table "
    if id:
        sql += f" WHERE id = {id}"
    cursor.execute(sql)

    #parte de printar
    columns = [i[0] for i in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=columns)
    json = df.to_json(orient="records")

    return json


def convert_dict_to_sql_string(data:dict, separator=",") -> str:
    converted_to_sql_data = []
    for key, value in data.items():
        if isinstance(value, str) and value.upper() != "DEFAULT" and value.upper() != "NULL":
            converted_to_sql_data.append(f"{key} = '{value}'")
        else:
            converted_to_sql_data.append(f"{key} = {value}")
    string_values = f"{separator}".join(converted_to_sql_data)
    return string_values

@app.route("/update/<int:id>", methods=['PUT'])
def update(id):
    raw_request = request.data.decode("utf-8")
    dict_values = json.loads(raw_request)
    frase_update = convert_dict_to_sql_string(dict_values, separator=",")

    sql = "UPDATE test_table SET "
    sql += frase_update
    sql += f" WHERE id = {id} "
    print(sql)
    try:
        affected_rows = cursor.execute(sql)
        if affected_rows > 0:
            return "Deu tudo certo!", 200
    except Exception as error:
        return str(error.args)
    return "Algo deu errado!", 400

#Toda vez que eu executo um arquivo, o __name__ vira __main__
if __name__ == "__main__":
    # o debug é para atualizar o servidor cada vez que eu atualizar o código
    app.run(debug=True)