from fastapi import APIRouter



router = APIRouter()
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


