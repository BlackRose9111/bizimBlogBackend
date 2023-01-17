from fastapi import APIRouter
from Models.DTO import CreateUserDTO



router = APIRouter()

@router.get("/")
async def hello():
    return {"message":"You found the authentication controller"}
@router.post("/login")
async def login(LoginDTO):
    from Models.Models import User
    from Authorization.Authorization import Authorization
    user = User.find_where(email=LoginDTO.email)
    if user == None:
        return
    if user.check_password(user.password):
        return {"message":"Login successful","token":Authorization.get_instance().generate_token(user)}
    return {"message":"Login failed"}


@router.post("/register")
async def register(RegisterDTO : CreateUserDTO):
    from Models.Models import User

    user = await User.find_where(email=RegisterDTO.email)
    if len(user) > 0:
        return {"message":"User already exists"}
    newUser = User(email=RegisterDTO.email,password=RegisterDTO.password,name=RegisterDTO.name,surname=RegisterDTO.surname)
    newUser.set_password(RegisterDTO.password)
    newUser.create()
    print(user.id+"Created")
    return {"message":"User created"}