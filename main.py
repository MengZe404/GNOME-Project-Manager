# Py-DMS (Development Management System)

# Features:
# Authentication System (Security)
# Database
# To-Do list
# Timer

from sys import exit
import sqlite3
import re
import datetime
import requests
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

        github_data = requests.get(f"https://api.github.com/users/{uname}")

        if github_data.status_code != 200:
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))

        data_set = github_data.json()

        company = data_set['company']
        location = data_set['location']
        follower = data_set['followers']
        
        insert = '''
            INSERT INTO users (id, github, pword, names, email, github_url, register_date, follower, company, user_location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        info = (id, uname, str(password.encrypt(id + 18, pword)), name, email, github, datetime.date.today(), follower, company, location)

        self.c.execute(insert, info)

        self.connection.commit()

    def createRepoDB(self, uname):
        github = self.c.execute('SELECT id FROM users WHERE github=?', (uname,))
        for i in github:
            id = i[0]
        repos = requests.get(f"https://api.github.com/users/{uname}/repos")

        if repos.status_code != 200:
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))

        insert = '''
            INSERT INTO repos (REPO_ID, repo_name, repo_url, created_date, repo_description, forks, repo_status, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        '''

        for repo in repos.json():
            repo_id = repo['id']
            repo_name = repo['name']
            repo_url = repo['html_url']
            repo_date = repo['created_at']
            repo_description = repo['description']
            repo_forks = repo['forks']
            repo_status = '1'
            self.c.execute(insert, (repo_id, repo_name, repo_url, repo_date, repo_description, repo_forks, repo_status, id))

        self.connection.commit()
        

    def varify(self, uname, pword):
        list = self.c.execute('SELECT id, github, pword FROM users')
        for i in list:
            if(i[1] == uname and password.decrypt(i[0] + 18, i[2]) == pword):
                return True
                
        return False

    def getRepoData(self, uname):
        data = self.c.execute('SELECT REPO_ID, repo_name, repo_url, created_date, forks, repo_status, user_id FROM repos JOIN users ON repos.user_id = users.id WHERE users.github=?', (uname, ))
        return data

    def getData(self, uname):
        data = self.c.execute('SELECT github, github_url, email, register_date, names, id, follower, company, user_location FROM users WHERE users.github=?', (uname,))
        return data
    
    def getRepoCount(self, uname):
        repo_count = self.c.execute('SELECT COUNT(REPO_ID) FROM repos INNER JOIN users ON repos.user_id = users.ID WHERE users.github=?', (uname,))
        for i in repo_count:
            repo_count = str(i)

        return repo_count[1]
    
    def updateData(self, uname, name, email, url, location, company):
        update = '''
        UPDATE users
        SET names=?, email=?, github_url=?, user_location=?, company=?
        WHERE github=?
        '''
        data = (name, email, url, location, company, uname)
        self.c.execute(update, data)
        self.connection.commit()

    def deleteAccount(self, id):
        self.c.execute('DELETE FROM users WHERE users.id = ?', (id,))
        self.connection.commit()
    
    def recoverAccount(self, email, uname):
        data = self.c.execute('SELECT id, pword FROM users WHERE users.email=? AND users.github=?', (email, uname))
        for i in data:
            return password.decrypt(i[0] + 18, i[1])

    def url_validate(self, str):
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return (re.match(regex, str) is not None)

    def toggle(self, status, id):
        self.c.execute("UPDATE repos SET repo_status=? WHERE REPO_ID=?", (status, id))
        self.connection.commit()

