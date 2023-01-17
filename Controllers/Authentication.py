from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from Models.DTO import CreateUserDTO,LoginDto



router = APIRouter()



@router.get("/")
async def hello():
    return {"message":"You found the authentication controller"}
@router.post("/login")
async def login(LoginDTO : LoginDto):
    from Models.Models import User
    from Authorization.Authorization import Authorization
    try:
        user = await User.find_where(email=LoginDTO.email)
        user = user[0]
    except:
        raise HTTPException(status_code=404, detail="User not found")
    if user == None:
        return
    if user.check_password(LoginDTO.password):
        return {"message":"Login successful","Authorization":Authorization.get_instance().generate_token(user)}
    else:
        raise HTTPException(status_code=401, detail="Incorrect password")


@router.post("/register")
async def register(request : Request):
    from Models.Models import User
    result = await request.json()
    RegisterDTO = CreateUserDTO(email=result["email"],name=result["name"],surname=result["surname"],password=result["password"])
    print(RegisterDTO)
    user = await User.find_where(email=RegisterDTO.email)
    if len(user) > 0:
        raise HTTPException(status_code=400, detail="Email already exists")
    newUser = User(email=result["email"],name=result["name"],surname=result["surname"])
    newUser.set_password(result["password"])
    newUser.create()
    print(f"{newUser.email} created")
    return {"message":"User created"}