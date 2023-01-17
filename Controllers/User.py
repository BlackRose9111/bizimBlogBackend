from fastapi import APIRouter, HTTPException
from fastapi.openapi.models import Header

from Models.DTO import CreateUserDTO

router = APIRouter()
@router.get("/test/")
async def test():
    return {"message": "Hello World"}

@router.get("/")
async def get_user(Authorization : str = Header(keyword="Authorization",default=None,description="Authorization token")):

    print(Authorization)
    from Models.DTO import DTO
    from Authorization.Authorization import Authorization
    user = Authorization.get_instance().get_user(Authorization)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")

    userdto = DTO(id=id,name=user.name,surname=user.surname,email=user.email)
    return userdto.to_json()

@router.post("/")
async def create_user(userdto: CreateUserDTO):
    from Models.Models import User
    from Models.DTO import DTO
    print(userdto)
    user = User(name=userdto.name,surname=userdto.surname,email=userdto.email)
    user.set_password(userdto.password)
    user.create()
    userdto = DTO(id=user.id,name=user.name,surname=user.surname,email=user.email)
    return {"message":"User created","user":userdto}
@router.put("/")
async def update_user(user,token):
    from Models.Models import User
    from Authorization.Authorization import Authorization
    from Models.DTO import DTO
    if Authorization.get_instance().get_user(token) == None:
        return {"message":"Unauthorized" }
    User = User.get(user.id)
    if User == None:
        return {"message":"User not found"}
    User.name = user.name
    User.surname = user.surname
    User.email = user.email
    User.password = user.password
    User.update()
    userdto = DTO(id=user.id,name=User.name,surname=User.surname,email=User.email)
    return {"message":"User updated","user":userdto.to_json()}
@router.delete("/")
async def delete_user(token):
    from Authorization.Authorization import Authorization
    user = Authorization.get_instance().get_user(token)
    if user == None:
        return {"message":"Unauthorized" }
    user.delete()
    return {"message":"User deleted"}
