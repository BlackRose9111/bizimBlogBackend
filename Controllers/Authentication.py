from fastapi import APIRouter, HTTPException

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
        return {"message":"Login successful","token":Authorization.get_instance().generate_token(user)}
    raise HTTPException(status_code=401, detail="Incorrect email or password")


@router.post("/register",status_code=200)
async def register(RegisterDTO : CreateUserDTO):
    from Models.Models import User

    user = await User.find_where(email=RegisterDTO.email)
    if len(user) > 0:
        raise HTTPException(status_code=400, detail="Email already exists")
    newUser = User(email=RegisterDTO.email,password=RegisterDTO.password,name=RegisterDTO.name,surname=RegisterDTO.surname)
    newUser.set_password(RegisterDTO.password)
    newUser.create()
    print(f"{newUser.email} created")
    return {"message":"User created"}