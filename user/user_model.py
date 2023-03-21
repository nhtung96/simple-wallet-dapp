import sqlite3 as sql

class UserAccount():
    def __init__(self):
        self.database = "user/database.db"
        self.username = ""
        self.password = ""

    def insertUser(self, username, password):
        if self._check_is_exist(username=username):
            return False, "Username is exist"
        
        con = sql.connect(self.database)
        cur = con.cursor() 
        cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username, password))
        con.commit()
        con.close()
        self.username = username
        self.password = password
        return True, ""


    def _check_is_exist(self, username):
        con = sql.connect(self.database)
        cur = con.cursor()
        cur.execute("SELECT username, password FROM users WHERE username='{}'".format(username))
        # users = cur.fetchall()
        
        if cur.fetchone() is None:
            con.close()
            return False
        else:
            con.close()
            return True

    def retrieveUsers(self, username, password):
        con = sql.connect(self.database)
        cur = con.cursor()
        cur.execute("SELECT username, password FROM users WHERE username='{}' and password ='{}'".format(username, password))
        # users = cur.fetchall()
        if cur.fetchone() is None:
            con.close()
            return False, "Account is not exist!"
        else:
            self.username = username
            self.password = password
            return True, ""
    
    def logout(self):
        self.username = ""
        self.password = ""