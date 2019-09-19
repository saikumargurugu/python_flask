import psycopg2
from flask import Flask,url_for,render_template
import itertools
app = Flask(__name__)
connection = psycopg2.connect(user="postgres",
                            password="unosimple",
                            host="localhost",
                            port="5432",
                            database="userinfo")
cursor = connection.cursor()
@app.route('/hello')
def hello_name():
   d=cursor.execute("""select * FROM userdataa""")
   connection.commit()
   l=[]
   g={}
   for row in d:
      g={'sno': row[0], 'uname': row[1], 'phno': row[2],'email':row[3]}
      l.append(g)
   return render_template('index.html', l=l)
   
@app.route('/man/<name>')
def hello_man(name):
   return 'hello %s' % name

@app.route('/user/<names>')
def user_into(names):
   if names == 'hello':
      return redirect(url_for('hello_name'))
   else:
      return redirect(url_for('hello_man',name = names))
   app.run(debug = True)
if __name__ == "__main__": 
    app.run(debug=True)