@app.route('/hello', methods=['GET','POST'])
def removedata():
   form= RemoveUser()
   if request.method =='POST':
      snoo=request.form['snoo']
      print(snoo)
      postgreSQL_select_Query="""DELETE  FROM userdataa WHERE sno = %s"""
      cursor.execute(postgreSQL_select_Query,(str(snoo),))
      return redirect(url_for('hello_name'))
   return render_template('index.html',form=form)