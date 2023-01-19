from time import sleep

from mysql import connector

instance  = None
import threading
class DbConnection:
    def __init__(self):
        from environment import getconfig
        self.connection = connector.connect(user=getconfig("DATABASE_USER"), password=getconfig("DATABASE_PASSWORD"), host=getconfig("DATABASE_HOST"), database=getconfig("DATABASE_NAME"))
        self.connection.autocommit = True
        self.cursor = self.connection.cursor(dictionary=True, buffered=True)
        self.keep_alive_thread = threading.Thread(target=self.keep_alive,daemon=True)
        self.keep_alive_thread.start()
    def __del__(self):
        self.connection.close()
        self.keep_alive_thread.join()
        print("Database connection closed")
        global instance
        instance = None

    def execute(self, query,params=None):
        print("Executing")
        self.cursor.execute(query,params)
        self.connection.commit()

    def last_id(self):
        print("Last id")
        return self.cursor.lastrowid

    def fetch(self, query,params=None):
        self.cursor.execute(query,params)
        print("Fetching")
        return self.cursor.fetchall()
    async def fetch_async(self, query,params=None):
        self.cursor.execute(query,params)
        print("Fetching async")
        return self.cursor.fetchall()



    def keep_alive(self):
        while(True):
            self.connection.ping(reconnect=True)
            print("Pinging database")
            sleep(120)

    def end(self):
        self.connection.close()
        self.keep_alive_thread.join()
        print("Database connection closed")
        instance = None
    @staticmethod
    def get_instance():
        global instance
        if instance is None:
            instance = DbConnection()
        return instance
