# Py-DMS (Development Management System)

# Features:
# Authentication System (Security)
# Database
# To-Do list
# Timer

from sys import exit
import sqlite3
import datetime
import password # My own module

# Sqlite3 Note - Connection & Cursor:
# A Connection object represents the database
# A Cursor provides functionalities

# Creat database if it doesn't exist
try:
    f = open("db/main.db", 'r').close()
except:
    open("db/main.db", 'w').close

    # If the database is empty, make tables
    sql = open('db/init.sql', "r")
    schema = sql.read()

    connection = sqlite3.connect('db/main.db')
    connection.executescript(schema) 
    connection.close()


class MyDMS(object):
    def __init__(self):
        # Connect to the database
        self.connection = sqlite3.connect('db/main.db')

        # Create cursor
        self.c = self.connection.cursor()

    def register(self, uname, pword, name, email, github):
        getId = "SELECT COUNT(id) FROM users"

        count = self.c.execute(getId)
        for i in count:
            id = i[0] + 1

        info = (id, uname, str(password.encrypt(id + 18, pword)), name, email, github, datetime.date.today())

        insert = '''
            INSERT INTO users (id, uname, pword, names, email, github, register_date)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        '''
        self.c.execute(insert, info)

        self.connection.commit()

    def varify(self, uname, pword):
        list = self.c.execute('SELECT id, uname, pword FROM users')
        for i in list:
            if(i[1] == uname and password.decrypt(i[0] + 18, i[2]) == pword):
                return True
                
        return False

    def getData(self, uname):
        data = self.c.execute('SELECT names, email, github, register_date FROM users WHERE uname=?', (uname, ))
        return data

    def deleteAccount(self, id):
        self.c.execute('DELETE FROM users WHERE users.id = ?', (id,))
        self.connection.commit()
    
    def recoverAccount(self, email):
        data = self.c.execute('SELECT id, pword FROM users WHERE users.email=?', (email,))
        for i in data:
            return password.decrypt(i[0] + 18, i[1])
