from fastapi import APIRouter, HTTPException
from fastapi.openapi.models import Header
from starlette.requests import Request
from starlette.responses import JSONResponse

import Models.DTO
from Models.DTO import *

router = APIRouter()
@router.get("/test/")
async def test():
    return {"message": "Hello World"}

@router.get("/")
async def get_user(request : Request):
    token = request.headers.get("authorization")

    from Models.DTO import DTO
    from Authorization.Authorization import Authorization
    user = Authorization.get_instance().get_user(token)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")

    userdto = Models.DTO.UserInfoDTO(id=user.id,name=user.name,surname=user.surname,email=user.email,superadmin=user.superadmin)
    print(userdto)
    return {"message":"User found","user":userdto}

@router.post("/")
async def create_user(userdto: CreateUserDTO):
    from Models.Models import User
    from Models.DTO import DTO
    print(userdto)
    user = User(name=userdto.name,surname=userdto.surname,email=userdto.email)
    user.set_password(userdto.password)
    try:
        user.create()
    except:
        raise HTTPException(status_code=500, detail="User could not be created")

    userdto = DTO(id=user.id,name=user.name,surname=user.surname,email=user.email)
    return {"message":"User created","user":userdto}
@router.put("/")
async def update_user(updateUserDTO : EditUserDTO, request : Request):
    from Models.Models import User
    from Authorization.Authorization import Authorization
    from Models.DTO import DTO
    token = request.headers.get("authorization")
    if Authorization.get_instance().get_user(token) == None:
        return {"message":"Unauthorized" }
    User = Authorization.get_instance().get_user(token)
    if User == None:
        return {"message":"User not found"}
    if updateUserDTO.name is not None and User.name != updateUserDTO.name:
        User.name = updateUserDTO.name
    if updateUserDTO.surname is not None and User.surname != updateUserDTO.surname:
        User.surname = updateUserDTO.surname
    if updateUserDTO.email is not None and User.email != updateUserDTO.email:
        User.email = updateUserDTO.email
    if updateUserDTO.password is not None and User.password != updateUserDTO.password:
        User.set_password(updateUserDTO.password)
    User.update()
    User.password = None
    try:
        User.update()
    except:
        raise HTTPException(detail="User could not be updated",status_code=500)
    userdto = UserInfoDTO(id=User.id,name=User.name,surname=User.surname,email=User.email,superadmin=User.superadmin)
    return {"message":"User updated","user":userdto}

async def delete_user(token):
    from Authorization.Authorization import Authorization
    user = Authorization.get_instance().get_user(token)
    if user == None:
        return {"message":"Unauthorized" }

    user.delete()
    return {"message":"User deleted"}
