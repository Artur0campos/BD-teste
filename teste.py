import mysql.connector

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="filiais_BD"
)

myCursor = dataBase.cursor()

myCursor.execute("insert into assinante_tbl (nome) values (%s)", ("Artur",) )
dataBase.commit()
