from fastapi import APIRouter



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
        return {"message":"User not found"}
    if user.check_password(user.password):
        return {"message":"Login successful","token":Authorization.get_instance().generate_token(user)}
    return {"message":"Login failed"}


@router.post("/register")
async def register(RegisterDTO):
    from Models.Models import User
    user = User.find_where(email=RegisterDTO.email)
    if user != None:
        return {"message":"User already exists"}
    user = User(**RegisterDTO.__dict__)
    user.set_password(user.password)
    user.create()
    return {"message":"User created"}