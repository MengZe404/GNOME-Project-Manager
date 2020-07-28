__name__ = "MyGPM"
__author__ = "MengZe"
__version__ = "1.0"

# Libraries
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


# Note: `uname` is always unique

class MyGPM(object):
    '''
    Help on module DMS

    Name
        dms

    Description
        This module provides access to SQL database (`main.db`)
        and GitHub API.

    Class
        MyDMS()

    Global Variable
        uname - GitHub Username (unique)

    Functions
        register(uname, pword, name, email, github)
            Register an user acocunt and record the data in SQL database
        
        createRepoDB(uname)
            Request all public repos infos from GitHub API (using uname) 
            and record in SQL database

        updateData(uname, name, email, url, location, company)
            Update the database with data
        
        getUsersData(uname)
            Get users data from SQL database (FROM users table)
            Return data

        getReposData(uname)
            Get repos data from SQL database (FROM repos table)
            Return data

        getRepoCount(uname)
            Count the number of repos (FROM repos table)
            Return repo_count

        varify(uname, pword)
            Varify the account with username and password

        refreshData(uname)
            Refresh the database

        deleteAccount(uname)
            Delete the account data (ALL) from SQL Database
        
        revoverAccount(email, uname)
            Get the password of the account with email and username
            Return password
    '''

    def __init__(self):
        # Connect to the database
        self.connection = sqlite3.connect('db/main.db')
        # Create cursor
        self.c = self.connection.cursor()

#### Create the database and add data
    # This allows the user to register an account
    def register(self, uname, pword, name, email, github):
        getId = "SELECT COUNT(id) FROM users"

        count = self.c.execute(getId)

        for i in count: # Let the id starts from 1
            id = i[0] + 1
        
        # Insert data to the database
        insert = '''
            INSERT INTO users (id, github, pword, names, email, github_url, register_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''

        info = (id, uname, str(password.encrypt(id + 18, pword)), name, email, github, datetime.date.today())

        self.c.execute(insert, info)
        self.connection.commit()


    def addUserData(self, uname):
        # Request data from GitHub API
        github_data = requests.get(f"https://api.github.com/users/{uname}")

        if github_data.status_code != 200:
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))

        data_set = github_data.json()

        company = data_set['company']
        location = data_set['location']
        follower = data_set['followers']

        update = '''
            UPDATE users 
            SET company=?, user_location=?, follower=?
            WHERE github=?
        '''

        info = (company, location, follower, uname)

        self.c.execute(update, info)
        self.connection.commit()


    # Get repo data from GitHub API
    def createRepoDB(self, uname):
        github = self.c.execute('SELECT id FROM users WHERE github=?', (uname,))

        for i in github:
            id = i[0]

        # Get repo data from GitHub API
        repos = requests.get(f"https://api.github.com/users/{uname}/repos")

        if repos.status_code != 200:
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))

        insert = '''
            INSERT INTO repos (REPO_ID, repo_name, repo_url, created_date, repo_description, forks, repo_status, user_id, repo_language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''

        for repo in repos.json():
            repo_id = repo['id']
            repo_name = repo['name']
            repo_language = repo['language']
            repo_url = repo['html_url']
            repo_date = repo['created_at']
            repo_description = repo['description']
            repo_forks = repo['forks']
            repo_status = '1'
            self.c.execute(insert, (repo_id, repo_name, repo_url, repo_date, repo_description, repo_forks, repo_status, id, repo_language))

        self.connection.commit()



#### Insert Data
    def insertProjectDB(self, uname, name, language, type, audience, feature, detail, path='', date='', todo='', repo_id=0, id=0):
        if date == '':
            date = datetime.date.today()

        github = self.c.execute('SELECT id FROM users WHERE github=?', (uname,))
        for i in github:
            user_id = i[0]

        if id == 0:
            getId = "SELECT COUNT(PROJECT_ID) FROM projects"
            count = self.c.execute(getId)
            for i in count: # Let the id starts from 1
                project_id = i[0] + 1
        else:
            project_id = id

        insert = '''
            INSERT INTO projects (PROJECT_ID, project_name, project_language, project_type, project_audience, project_feature, project_detail, project_path, project_date, project_status, project_todo, user_id, repo_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''

        self.c.execute(insert, (project_id, name, language, type, audience, feature, detail, path, date, 0, todo, user_id, repo_id))

        self.connection.commit()

    
    def insertIdeaDB(self, uname, name, language, type, audience, feature, detail):

        date = datetime.date.today()

        github = self.c.execute('SELECT id FROM users WHERE github=?', (uname,))
        for i in github:
            user_id = i[0]

        getId = "SELECT COUNT(IDEA_ID) FROM ideas"
        count = self.c.execute(getId)
        for i in count: # Let the id starts from 1
            idea_id = i[0] + 1

        insert = '''
            INSERT INTO ideas (IDEA_ID, idea_name, idea_language, idea_type, idea_audience, idea_feature, idea_detail, idea_date, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''

        self.c.execute(insert, (idea_id, password.encrypt(8, name), language, type, audience, password.encrypt(8, feature), password.encrypt(8, detail), date, user_id))

        self.connection.commit()
        return 1

    def insertResourceDB(self, id, name, url):
        self.c.execute("INSERT INTO resources (project_id, resource_title, resource_url) VALUES(?, ?, ?)", (id, name, url))
        self.connection.commit()

    def insertSearchDB(self, id, name, url):
        self.c.execute("INSERT INTO search_history (project_id, question, search_url) VALUES(?, ?, ?)", (id, name, url))
        self.connection.commit()



#### Update Data
    def updateUserData(self, uname, name, email, url, location, company):
        update = '''
        UPDATE users
        SET names=?, email=?, github_url=?, user_location=?, company=?
        WHERE github=?
        '''
        data = (name, email, url, location, company, uname)
        self.c.execute(update, data)
        self.connection.commit()


    def updateIdeaData(self, id, name, language, type, audience, feature, detail):
        update = '''
        UPDATE ideas
        SET idea_name=?, idea_language=?, idea_type=?, idea_audience=?, idea_feature=?, idea_detail=?
        WHERE IDEA_ID=?
        '''
        data = (password.encrypt(8, name), language, type, audience, password.encrypt(8, feature), password.encrypt(8, detail), id)
        self.c.execute(update, data)
        self.connection.commit()

    def updateProjectData(self, id, name, language, type, audience, feature, detail, path):
        update = '''
        UPDATE projects
        SET project_name=?, project_language=?, project_type=?, project_audience=?, project_feature=?, project_detail=?, project_path=?
        WHERE PROJECT_ID=?
        '''
        data = (name, language, type, audience, feature, detail, path, id)
        self.c.execute(update, data)
        self.connection.commit()

    def updateTodo(self, id, todo):
       self.c.execute("UPDATE PROJECTS SET project_todo=? WHERE PROJECT_ID=?", (todo, id))
       self.connection.commit()


#### Refresh & Delete data
    def refreshData(self, uname):
        self.c.execute('DELETE FROM repos WHERE repos.user_id=(SELECT ID FROM users WHERE github=?)', (uname,))
        self.connection.commit()
        self.createRepoDB(uname)

    def deleteIdea(self, id):
        self.c.execute("DELETE FROM ideas WHERE IDEA_ID=?", (id,))
        self.c.execute("UPDATE ideas SET IDEA_ID=IDEA_ID - 1 WHERE IDEA_ID > ?", (id,))
        self.connection.commit()

    def clearHistory(self, id):
        self.c.execute("DELETE FROM search_history WHERE project_id=?", (id,))
        self.connection.commit()

    def clearResource(self, id):
        self.c.execute("DELETE FROM resources WHERE project_id=?", (id,))
        self.connection.commit()


#### Get data from the database
    def getUsersData(self, uname):
        data = self.c.execute('SELECT github, github_url, email, register_date, names, id, follower, company, user_location FROM users WHERE users.github=?', (uname,))
        return data
    
    def getReposData(self, uname):
        data = self.c.execute('SELECT REPO_ID, repo_name, repo_url, created_date, forks, repo_status, user_id FROM repos JOIN users ON repos.user_id = users.id WHERE users.github=?', (uname, ))
        return data

    def getIdeaData(self, id):
        data = self.c.execute("SELECT IDEA_ID, idea_name, idea_language, idea_type, idea_audience, idea_feature, idea_detail, idea_date FROM ideas WHERE IDEA_ID=?", (id,))
        return data

    def getProjectWorking(self, uname):
        project_working = self.c.execute('SELECT PROJECT_ID, project_name, project_path FROM projects INNER JOIN users ON projects.user_id=users.ID WHERE users.github=? AND projects.project_status=0', (uname,))
        return project_working

    
    def getProjectData(self, id):
        project =  self.c.execute('SELECT project_name, project_language, project_type, project_audience, project_feature, project_detail, project_path, project_date FROM projects WHERE PROJECT_ID=?', (id,))
        return project


    def getRepoCount(self, uname):
        repo_count = self.c.execute('SELECT COUNT(REPO_ID) FROM repos INNER JOIN users ON repos.user_id = users.ID WHERE users.github=?', (uname,))
        for i in repo_count:
            repo_count = i[0]
        return repo_count

    def getIdeaCount(self, uname):
        idea_count = self.c.execute('SELECT COUNT(IDEA_ID) FROM ideas INNER JOIN users ON ideas.user_id = users.ID WHERE users.github=?', (uname,))
        for i in idea_count:
            idea_count = i[0]
        return idea_count

    def getTodo(self, id):
        todo = self.c.execute('SELECT project_todo FROM projects WHERE PROJECT_ID=?', (id,))
        for i in todo:
            todo = i[0]
        return todo


    def getRepoStatus(self, id):
        repo_status = self.c.execute("SELECT repo_status FROM repos WHERE REPO_ID=?", (id,))
        for i in repo_status:
            repo_status = i[0]
        return repo_status

    def getResources(self, id):
        data = self.c.execute("SELECT * FROM resources WHERE project_id=?", (id,))
        return data

    def getHistory(self, id):
        data = self.c.execute("SELECT * FROM search_history WHERE project_id=?", (id,))
        return data


#### Login System   
    def varify(self, uname, pword):
        list = self.c.execute('SELECT id, github, pword FROM users')
        for i in list:
            if(i[1] == uname and password.decrypt(i[0] + 18, i[2]) == pword):
                return True
                
        return False

    
    def checkAccount(self, uname):
        data = self.c.execute("SELECT ID FROM users WHERE github=?", (uname, ))
        for i in data:
            return True

        return False


    def deleteAccount(self, uname):
        self.c.execute('DELETE FROM repos WHERE repos.user_id=(SELECT ID FROM users WHERE github=?)', (uname,))
        self.c.execute('DELETE FROM projects WHERE projects.user_id=(SELECT ID FROM users WHERE github=?)', (uname,))
        self.c.execute('DELETE FROM users WHERE users.github = ?', (uname,))
        self.connection.commit()
    

    def recoverAccount(self, email, uname):
        data = self.c.execute('SELECT id, pword FROM users WHERE users.email=? AND users.github=?', (email, uname))
        for i in data:
            return password.decrypt(i[0] + 18, i[1])


    # Thanks to: https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45
    def url_validate(self, str):
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return (re.match(regex, str) is not None)


#### Utilities
    def toggleRepo(self, status, id, uname):
        self.c.execute("UPDATE repos SET repo_status=? WHERE REPO_ID=?", (status, id))

        if status == 0:
            repo_data = self.c.execute('SELECT REPO_ID, repo_name, repo_url, created_date, repo_description, repo_language FROM repos WHERE REPO_ID=?', (id,))
            for i in repo_data:
                data = i
            self.insertProjectDB(uname, data[1], language=data[5], type='', audience='', feature='', detail=data[4], path='', date=data[3], repo_id=data[0], id=data[0])
        if status == 1:
            self.c.execute('DELETE FROM projects WHERE projects.repo_id=?', (id,))
        
        self.connection.commit()

    def toggleProject(self, status, id, uname):
        try:
            repo_id = self.c.execute("SELECT repos.REPO_ID FROM repos INNER JOIN projects ON repos.REPO_ID=projects.repo_id WHERE projects.PROJECT_ID=?", (id,))
            for i in repo_id:
                repo_id = i[0]
            self.c.execute("UPDATE repos SET repo_status=1 WHERE REPO_ID=?", (repo_id,))
        except:
            pass

        if status == 1:
            self.c.execute('DELETE FROM projects WHERE projects.PROJECT_ID=?', (id,))
        
        self.connection.commit()

