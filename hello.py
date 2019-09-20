import psycopg2
from flask import Flask,url_for,render_template, request, redirect, flash
import itertools
from forms import AddDataForm,RemoveUser,UpdateUser
import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
#app.config['SECRET-KEY']='dd916e7b012cdd2b8ed48d32f35fc9ee'

connection = psycopg2.connect(user="postgres",
                            password="unosimple",
                            host="localhost",
                            port="5432",
                            database="userinfo")
cursor = connection.cursor()
@app.route('/hello', methods=['GET','POST'])
def hello_name():
   form= RemoveUser()
   cursor.execute("""select * FROM userdataa""")
   d=cursor.fetchall()
   connection.commit()
   l=[]
   for row in d:
      g={'sno': row[0], 'uname': row[1], 'phno': row[2],'email':row[3]}
      l.append(g)
   if request.method =='POST':
      snoo=request.form['s']
      print(snoo)
      postgreSQL_select_Query="""DELETE  FROM userdataa WHERE sno = %s"""
      cursor.execute(postgreSQL_select_Query,(str(snoo),))
      return redirect(url_for('hello_name'))
   return render_template('index.html',form=form, l=l)
@app.route('/adddata', methods=['GET','POST'])
def adddata():
   form = AddDataForm()
   if request.method =='POST':
         uname=request.form['uname']
         phno=request.form['phno']
         email=request.form['email']
         result= email.find('@')
         if result >= 1:
            result=email.find('.')
            if  result >= 1:
                  if len(phno) == 10: 
                     postgreSQL_select_Query = """ INSERT INTO userdataa( uname, phno, email) VALUES (%s,%s,%s)"""
                     datainsert = ( uname, phno, email)
                     cursor.execute(postgreSQL_select_Query, datainsert)
                     connection.commit()
                     return redirect(url_for('hello_name'))
                  else:
                     flash(f'incorrect moblile number, plese make sure that lenth is correct { phno } ', 'success')
            else:
               flash(f'email domain error (.) {email} ', 'success')
         else:
            flash(f'email domain error _@_ {email} ', 'success')
   return render_template('add.html',form=form)

@app.route('/upuser', methods=['GET','POST'])
def updatedata():
   form = UpdateUser()
   if request.method =='POST':
      sno=request.form['sno']
      uname=request.form['uname']
      phno=request.form['phno']
      email=request.form['email']
      result= email.find('@')
      if request.form['uname'] :
         sql = """ UPDATE userdataa SET uname = (%s) WHERE sno = (%s)"""
         cursor.execute(sql,(str(uname),sno ))
         connection.commit()
      if request.form['phno'] :
         sql = """ UPDATE userdataa SET phno = (%s) WHERE sno = (%s)"""
         cursor.execute(sql,(str(phno),sno ))
         connection.commit()
      if request.form['email'] :
         sql = """ UPDATE userdataa SET email = (%s) WHERE sno = (%s)"""
         cursor.execute(sql,(str(email),sno ))
         connection.commit()
      return redirect(url_for('hello_name'))
   return render_template('update.html',form=form)

if __name__ == "__main__": 
    app.run(debug=True)