
import psycopg2
from flask import Flask, jsonify

connection = psycopg2.connect(user="postgres",
                            password="unosimple",
                            host="localhost",
                            port="5432",
                            database="userinfo")
cur =connection.cursor()
cur.execute('''SELECT * FROM userdataa WHERE sno=10''')
rv = cur.fetchall()
payload = []
content = {}
for result in rv:
    content = {'id': result[0], 'username': result[1], 'password': result[2]}
    payload.append(content)
    content = {}
p= jsonify(payload)
print(p)

