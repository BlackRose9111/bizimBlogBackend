from datetime import datetime

from Data.DbContext import DbConnection
import bcrypt

class Model():
    id : int = None
    dbinstance = None
    def __init__(self):
        self.dbinstance = DbConnection.get_instance()
    def create(self):
        pass
    def update(self):
        pass
    def delete(self):
        pass
    def jsonize(self):
        for key in getattr(self,"__annotations__"):
            if getattr(self,key) == None:
                setattr(self,key,"")
        from json import dumps
        return dumps(self.__dict__)

    @staticmethod
    def get(id):
        pass
    @staticmethod
    async def get_all():
        pass
    @staticmethod
    async def find_where(self,**kwargs):
        pass


class User(Model):
    name : str = None
    surname : str = None
    email : str = None
    password : str = None
    superadmin : bool = False
    def __init__(self,**kwargs):
        super().__init__()
        for key,value in kwargs.items():
            setattr(self,key,value)


    def create(self):
        self.dbinstance.execute("INSERT INTO user (name,surname,email,password) VALUES (%s,%s,%s,%s)",(self.name,self.surname,self.email,self.password))
        self.id = self.dbinstance.last_id()
        print("User created with id: ",self.id)
        return self.id
    def set_password(self,password):
        self.password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
    def check_password(self,password):
        encoded_password = password.encode('utf-8')
        encoded_hash = self.password.encode('utf-8')
        print(f"{encoded_password} Encoded Hash {encoded_hash}")
        return bcrypt.checkpw(password.encode("utf-8"),encoded_hash)

    def update(self):
        if self.id == None:
            return False
        self.dbinstance.execute("UPDATE user SET name=%s,surname=%s,email=%s,password=%s WHERE id=%s",(self.name,self.surname,self.email,self.password,self.id))
        print("User updated with id: ",self.id)
        return True
    def delete(self):
        if self.id == None:
            return False
        self.dbinstance.execute("DELETE FROM user WHERE id=%s",(self.id,))
        print("User deleted with id: ",self.id)
        return True
    @staticmethod
    def get(id):
        dbinstance = DbConnection.get_instance()
        try:
            user = dbinstance.fetch("SELECT * FROM user WHERE id=%s",(id,))[0]
        except:
            return None
        if user == None:
            return None
        return User(**user)
    @staticmethod
    async def get_all():
        dbinstance = DbConnection.get_instance()
        users = dbinstance.fetch("SELECT * FROM user WHERE 1")
        if users == None:
            return None
        return [User(**user) for user in users]
    @staticmethod
    async def find_where(**kwargs):
        dbinstance = DbConnection.get_instance()
        query = "SELECT * FROM user WHERE "
        values = []
        for key,value in kwargs.items():
            query += key + "=%s AND "
            values.append(value)
        query = query[:-4]
        users = dbinstance.fetch(query,values)
        if users == None:
            return None
        return [User(**user) for user in users]

class Blog(Model):
    author : User = None
    title : str = None
    content : str = None
    created : datetime = None
    updated : datetime = None
    def __init__(self,**kwargs):
        super().__init__()
        for key,value in kwargs.items():
            setattr(self,key,value)
    def create(self):
        self.dbinstance.execute("INSERT INTO blog (author,title,content,created,updated) VALUES (%s,%s,%s,%s,%s)",(self.author.id,self.title,self.content,self.created,self.updated))
        self.id = self.dbinstance.last_id()
        print("Blog created with id: ",self.id)
        return self.id

    def update(self):
        if self.id == None:
            return False
        self.dbinstance.execute("UPDATE blog SET author=%s,title=%s,content=%s,created=%s,updated=%s WHERE id=%s",(self.author.id,self.title,self.content,self.created,self.updated,self.id))
        print("Blog updated with id: ",self.id)
        return True

    def delete(self):
        if self.id == None:
            return False
        self.dbinstance.execute("DELETE FROM blog WHERE id=%s",(self.id,))
        print("Blog deleted with id: ",self.id)
        return True

    @staticmethod
    def get(id):
        dbinstance = DbConnection.get_instance()
        try:
            blog = dbinstance.fetch("SELECT * FROM blog WHERE id=%s",(id,))[0]
        except:
            return None
        if blog == None:
            return None
        blog["author"] = User.get(blog["author"])
        return Blog(**blog)
    @staticmethod
    async def get_all():
        dbinstance = DbConnection.get_instance()
        blogs = dbinstance.fetch("SELECT * FROM blog WHERE 1")
        if blogs == None:
            return None
        return [Blog(**blog) for blog in blogs]
    @staticmethod
    async def find_where(**kwargs):
        dbinstance = DbConnection.get_instance()
        query = "SELECT * FROM blog WHERE "
        values = []
        for key,value in kwargs.items():
            query += key + "=%s AND "
            values.append(value)
        query = query[:-4]
        blogs = dbinstance.fetch(query,values)
        if blogs == None:
            return None
        return [Blog(**blog) for blog in blogs]

