import sqlite3 as s


class DAL:
    filename="users.db"
    def __init__(self):
        self._initialize()
            
    def exec(self, SQL):
        with s.connect(self.filename) as con:
            cur = con.cursor()
            cur.execute(SQL)
            rows = cur.fetchall()
            return rows

    def _initialize(self):
        self.exec("CREATE TABLE IF NOT EXISTS users ('username',email,'password')")

    def add(self,username,email,password):
        checkExiststing = self.exec(f"SELECT username,email,password FROM users WHERE username='{username}' and email='{email}'")
        if len(checkExiststing) == 0:
            self.exec(f"INSERT INTO users VALUES ('{username}','{email}','{password}')")
            return True
        else:
            return 'The user alaredy exists'




class User:
    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
           return self.username
    
    def register(self):
        return DAL().add(self.username,self.email,self.password)
