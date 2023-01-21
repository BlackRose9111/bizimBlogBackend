import pydantic
from pydantic import BaseModel, Field


class DTO(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def __str__(self):
        return str(self.__dict__)



    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        from json import dumps
        return dumps(self.__dict__)
class CreateUserDTO(DTO):
    name : str = Field(max_length=50,description="Name of the user",example="John",title="Name",min_length=2,regex="^[a-zA-Z]+$")
    surname : str = Field(max_length=50,description="Surname of the user",example="Doe",title="Surname",min_length=2,regex="^[a-zA-Z]+$")
    email : str = Field(max_length=50,description="Email of the user",regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",example="BlackRose@crownmail.net")
    password : str = Field(max_length=50,description="Password of the user",example="123456",min_length=6,regex="^[a-zA-Z0-9]+$")

class EditBlogDTO(DTO):
    title : str = None
    content : str = None
    id : int = None
    author : int = None
    category : int = None
    description : str = None
class CreateBlogDTO(DTO):

    title : str = None
    content : str = None
    category : int = None
    description : str = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class LoginDto(DTO):
    email : str = None
    password : str = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class UserInfoDTO(DTO):
    id : int = None
    name : str = None
    surname : str = None
    email : str = None
    superadmin : bool = False

class CreateCategoryDTO(DTO):
    name : str = None

class EditUserDTO(DTO):
    name : str = None
    surname : str = None
    email : str = None
    password : str = None
    superadmin : bool = False

