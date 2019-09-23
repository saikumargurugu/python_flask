import psycopg2

connection = psycopg2.connect(user="postgres",
                            password="sai81432021",
                            host="localhost",
                            port="5432",
                            database="userinfo")
cursor = connection.cursor()
choice=int(input("select your option \n 1. add \n 2. delet \n 3. view \n 4. update \n"))
if choice ==1:
    uname = input("enter name:")
    phno = input("enter mobile no:")
    email = input("enter email id:")
    result= email.find('@')
    if result >= 1:
        result=email.find('.')
        if  result >= 1:
            if len(phno) == 10: 
                postgreSQL_select_Query = """ INSERT INTO userdataa( uname, phno, email) VALUES (%s,%s,%s)"""
                datainsert = ( uname, phno, email)
                cursor.execute(postgreSQL_select_Query, datainsert)
                connection.commit()
                count = cursor.rowcount
                print(count, "Record inserted successfully into table")
            else:
                print("please a mobile number of length 10")
        else:
            print("please enter a valid email id'DOMAIN ERROR .'.")
    else:
            print("please enter a valid email id 'DOMAIN ERRO @'.")
if choice == 2:
    delopt=input("enter the seial number of the user:")
    postgreSQL_select_Query="""DELETE  FROM userdataa WHERE sno = %s"""
    cursor.execute(postgreSQL_select_Query,str(delopt,))
    connection.commit()
if choice== 3:
    cursor.execute("""select * FROM userdataa""")
    connection.commit()
    d=cursor.fetchall()
    l=[]
    g={}
    for row in d:
        g={'sno': row[0], 'uname': row[1], 'phno': row[2],'email':row[3]}
        l.append(g)
    print(l)    

if choice== 4:
    cursor.execute("select * from userdataa")
    connection.commit()
    d=cursor.fetchall()
    for row in d:
         print("sno =  uname =  email=  phno =  ")   
         print( row[0],"  ", row[1],"  " ,row[2],"  ",row[3])
    udata= input("enter the id of the user")
    csel= int(input("select the category \n 1.uname \n 2.phno \n 3.email \n"))
    if csel==1:
        ndata= input("\n enter new name")
        sql = """ UPDATE userdataa SET uname = (%s) WHERE sno = (%s)"""
        cursor.execute(sql,(ndata ,str(csel) ))
        connection.commit()
    if csel==2:
        ndata= int(input("\n enter new phno"))
        if len(ndata)==10:
            sql = """ UPDATE userdataa SET phno = (%s) WHERE sno = (%s)"""
            cursor.execute(sql,(ndata ,str(csel) ))
            connection.commit()
        else:
            print("please enter correct number")
    if csel==3:
        ndata= input("\n enter new data")
        if email.partition("@"): 
            sql = """ UPDATE userdataa SET email = (%s) WHERE sno = (%s)"""
            cursor.execute(sql,(ndata ,str(csel) ))
            connection.commit()
        else:
            print("Please enter correct email id")
    