from mysql import connector
from environment import configvariables, load_config
instance  = None
class DbConnection:
    def __init__(self):
        from environment import getconfig
        self.connection = connector.connect(user=getconfig("DATABASE_USER"), password=getconfig("DATABASE_PASSWORD"), host=getconfig("DATABASE_HOST"), database=getconfig("DATABASE_NAME"))
        self.cursor = self.connection.cursor(dictionary=True, buffered=True)
    def __del__(self):
        self.connection.close()

    def execute(self, query,params=None):
        self.cursor.execute(query,params)
        self.connection.commit()

    def last_id(self):
        return self.cursor.lastrowid

    def fetch(self, query,params=None):
        self.cursor.execute(query,params)
        return self.cursor.fetchall()
    async def fetch_async(self, query,params=None):
        self.cursor.execute(query,params)
        return self.cursor.fetchall()

    @staticmethod
    def get_instance():
        global instance
        if instance is None:
            instance = DbConnection()
        return instance
