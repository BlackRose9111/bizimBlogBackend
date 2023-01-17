import pydantic


class DTO(pydantic.BaseModel):
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
    name : str = None
    surname : str = None
    email : str = None
    password : str = None


class CreateBlogDTO(DTO):
    id : int = None
    title : str = None
    content : str = None
    author : int = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class LoginDto(DTO):
    email : str = None
    password : str = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class UserInfoDTO(DTO):
    name : str = None
    surname : str = None
    email : str = None
    superadmin : bool = False
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
