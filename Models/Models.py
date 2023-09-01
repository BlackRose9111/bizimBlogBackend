from datetime import datetime
from typing import List, Any

import pydantic

from Data.DbContext import DbConnection
import bcrypt


class Model(pydantic.BaseModel):
    id: int = None

    def __init__(self):
        super().__init__()

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def jsonize(self):
        for key in getattr(self, "__annotations__"):
            if getattr(self, key) == None:
                setattr(self, key, "")
        from json import dumps
        return dumps(self.__dict__)

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def get(id):
        pass

    @staticmethod
    async def get_all():
        pass

    @staticmethod
    async def find_where(self, **kwargs):
        pass


class User(Model):
    name: str = None
    surname: str = None
    email: str = None
    password: str = None
    superadmin: bool = False

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def create(self):
        context = DbConnection.get_instance()
        context.execute("INSERT INTO user (name,surname,email,password) VALUES (%s,%s,%s,%s)",
                        (self.name, self.surname, self.email, self.password))
        self.id = context.last_id()
        print("User created with id: ", self.id)
        return self.id

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        encoded_password = password.encode('utf-8')
        encoded_hash = self.password.encode('utf-8')
        print(f"{encoded_password} Encoded Hash {encoded_hash}")
        return bcrypt.checkpw(password.encode("utf-8"), encoded_hash)

    def update(self):
        if self.id == None:
            return False
        context = DbConnection.get_instance()

        context.execute("UPDATE user SET name=%s,surname=%s,email=%s,password=%s WHERE id=%s",
                        (self.name, self.surname, self.email, self.password, self.id))
        print("User updated with id: ", self.id)
        return True

    def delete(self):
        if self.id == None:
            return False
        context = DbConnection.get_instance()
        context.execute("DELETE FROM user WHERE id=%s", (self.id,))
        print("User deleted with id: ", self.id)
        return True

    @staticmethod
    def get(id):
        dbinstance = DbConnection.get_instance()
        try:
            user = dbinstance.fetch("SELECT * FROM user WHERE id=%s", (id,))[0]
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
        for key, value in kwargs.items():
            query += key + "=%s AND "
            values.append(value)
        query = query[:-4]
        users = dbinstance.fetch(query, values)
        if users == None:
            return None
        return [User(**user) for user in users]


class Category(Model):
    name: str = None

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def create(self):
        context = DbConnection.get_instance()
        context.execute("INSERT INTO category (name) VALUES (%s)", (self.name,))
        self.id = context.dbinstance.last_id()
        print("Category created with id: ", self.id)
        return self.id

    def update(self):
        if self.id == None:
            return False
        context = DbConnection.get_instance()
        context.execute("UPDATE category SET name=%s WHERE id=%s", (self.name, self.id))
        print("Category updated with id: ", self.id)
        return True

    def delete(self):
        if self.id == None:
            return False
        context = DbConnection.get_instance()
        context.execute("DELETE FROM category WHERE id=%s", (self.id,))
        print("Category deleted with id: ", self.id)
        return True

    @staticmethod
    def get(id):
        dbinstance = DbConnection.get_instance()
        try:
            categorydict = dbinstance.fetch("SELECT * FROM category WHERE id=%s", (id,))[0]
        except:
            return None
        if categorydict == None:
            return None
        return Category(id=categorydict["id"], name=categorydict["name"])

    @staticmethod
    async def get_all():
        dbinstance = DbConnection.get_instance()
        categories = dbinstance.fetch("SELECT * FROM category WHERE 1")
        if categories == None:
            return None
        return [category(**category) for category in categories]

    @staticmethod
    async def find_where(**kwargs):
        dbinstance = DbConnection.get_instance()
        query = "SELECT * FROM category WHERE "
        values = []
        for key, value in kwargs.items():
            query += key + "=%s AND "
            values.append(value)
        query = query[:-4]
        categories = dbinstance.fetch(query, tuple(values))
        if categories == None:
            return None
        return [category(**category) for category in categories]


class Blog(Model):
    author: User = None
    title: str = None
    content: str = None
    description: str = None
    created: datetime = None
    updated: datetime = None

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def create(self):
        context = DbConnection.get_instance()

        if type(self.author) == User:
            author = self.author.id
        else:
            author = self.author

        context.execute(
            "INSERT INTO blog (author,title,content,created,updated,description) VALUES (%s,%s,%s,%s,%s,%s)",
            (author, self.title, self.content, self.created, self.updated, self.description))
        self.id = context.last_id()
        self.created = datetime.now()
        self.updated = datetime.now()
        print("Blog created with id: ", self.id)
        return self.id

    def update(self):
        if self.id == None:
            return False
        context = DbConnection.get_instance()
        if self.author == None:
            author = None
        else:
            author = self.author.id

        context.execute(
            "UPDATE blog SET author=%s,title=%s,content=%s,created=%s,updated=%s, description =%s WHERE id=%s",
            (author, self.title, self.content, self.created, self.updated, self.author, self.description,
             self.id))
        print("Blog updated with id: ", self.id)
        return True

    def delete(self):
        if self.id == None:
            return False
        context = DbConnection.get_instance()
        context.execute("DELETE FROM blog WHERE id=%s", (self.id,))
        print("Blog deleted with id: ", self.id)
        return True

    @staticmethod
    def get(id):
        dbinstance = DbConnection.get_instance()
        try:
            blog = dbinstance.fetch("SELECT * FROM blog WHERE id=%s", (id,))[0]
        except:
            return None
        if blog == None:
            return None
        author = User.get(blog["author"])
        author.password = None
        blog["author"] = author
        return Blog(**blog)

    @staticmethod
    async def get_all():
        dbinstance = DbConnection.get_instance()
        blogs = dbinstance.fetch("SELECT * FROM blog WHERE 1 ORDER BY created DESC")
        if blogs == None:
            return None
        bloglist = [Blog(**blog) for blog in blogs]
        for blog in bloglist:
            author = User.get(blog.author)
            author.password = None
            blog.author = author

        return bloglist

    @staticmethod
    async def find_where(**kwargs):
        dbinstance = DbConnection.get_instance()
        query = "SELECT * FROM blog WHERE "
        values = []
        for key, value in kwargs.items():
            query += key + "=%s AND "
            values.append(value)
        query = query[:-4]
        blogs = dbinstance.fetch(query, tuple(values))
        if blogs == None:
            return None
        return [Blog(**blog) for blog in blogs]

    @staticmethod
    async def search(searchParameter, start=None, limit=None):
        dbinstance = DbConnection.get_instance()
        searchParameter = "%" + searchParameter + "%"
        if start == None:
            start = 0
        if limit == None:
            limit = 10
        blogs = dbinstance.fetch(
            "SELECT * FROM blog WHERE title LIKE %s OR content LIKE %s OR description LIKE %s ORDER BY created DESC LIMIT %s,%s",
            (searchParameter, searchParameter, searchParameter, start, limit))
        if blogs == None:
            return None
        bloglist = [Blog(**blog) for blog in blogs]
        for blog in bloglist:
            author = User.get(blog.author)
            author.password = None
            blog.author = author

        return bloglist


class blogCategory(Model):
    blog: Blog = None
    category: Category = None

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def create(self):
        context = DbConnection.get_instance()

        if type(self.blog) == Blog:
            blog = self.blog.id
        else:
            blog = self.blog

        if type(self.category) == Category:
            category = self.category.id
        else:
            category = self.category

        context.execute("INSERT INTO blogCategory (blogid,categoryId) VALUES (%s,%s)", (blog, category))
        self.id = context.last_id()
        print("blogCategory created with id: ", self.id)
        return self.id

    def delete(self):
        if self.id == None:
            return False
        context = DbConnection.get_instance()
        context.execute("DELETE FROM blogCategory WHERE blogCategoryId=%s", (self.id,))
        print("blogCategory deleted with id: ", self.id)
        return True

    @staticmethod
    def add_category_to_a_blog(blog: Blog, category: Category):
        # first we check if there  is already an entry for this blog and category
        dbInstance = DbConnection.get_instance()
        try:
            blogCategoryDict = \
            dbInstance.fetch("SELECT * FROM blogCategory WHERE blogid=%s AND categoryId=%s", (blog.id, category.id))[0]
        except:
            return None
        # if there is already an entry here, do nothing
        if blogCategoryDict != None:
            return True
        # if there is no entry, create one
        blogCategoryDict = {"blogid": blog.id, "categoryId": category.id}
        freshlycreatedcategory = blogCategory(**blogCategoryDict)
        freshlycreatedcategory.create()
        return True

    @staticmethod
    def get(id):
        dbInstance = DbConnection.get_instance()
        try:
            blogCategoryDict = dbInstance.fetch("SELECT * FROM blogCategory WHERE blogCategoryId=%s", (id,))[0]
        except:
            return None
        if blogCategoryDict == None:
            return None
        blogCategoryDict["blog"] = Blog.get(blogCategoryDict["blogid"])
        blogCategoryDict["category"] = Category.get(blogCategoryDict["categoryId"])
        return blogCategory(**blogCategoryDict)

    @staticmethod
    def get_all():
        dbInstance = DbConnection.get_instance()
        blogCategories = dbInstance.fetch("SELECT * FROM blogCategory WHERE 1")
        if blogCategories == None:
            return None
        listofblogCategories: list[blogCategories] = [blogCategory(**blogCategory) for blogCategory in blogCategories]
        # we will convert category and blog ids to objects
        for individual in listofblogCategories:
            individual.blog = Blog.get(individual.blog)
            individual.category = Category.get(individual.category)
        return listofblogCategories

    @staticmethod
    def find_where(**kwargs):
        dbInstance = DbConnection.get_instance()
        query = "SELECT * FROM blogCategory WHERE "
        values = []
        for key, value in kwargs.items():
            query += key + "=%s AND "
            values.append(value)
        query = query[:-4]
        blogCategories = dbInstance.fetch(query, tuple(values))
        if blogCategories == None:
            return None
        listOfCategories: list[blogCategories] = [blogCategory(**blogCategory) for blogCategory in blogCategories]
        # we will convert category and blog ids to objects
        for individual in listOfCategories:
            individual.blog = Blog.get(individual.blog)
            individual.category = Category.get(individual.category)
        return listOfCategories
    @staticmethod
    def get_all_categories_of_a_blog(blog: Blog):
        dbInstance = DbConnection.get_instance()
        blogCategories = dbInstance.fetch("SELECT categoryId FROM blogCategory WHERE blogid=%s", (blog.id,))
        #only return the category objects in a list
        return [Category.get(category["categoryId"]) for category in blogCategories]

