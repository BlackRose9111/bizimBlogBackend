from main import app

@app.post("/login")
async def login(user):
    from Models.Models import User
    from Authorization.Authorization import Authorization
    user = User.find_where(email=user.email)
    if user == None:
        return {"message":"User not found"}
    if user.check_password(user.password):
        return {"message":"Login successful","token":Authorization.get_instance().generate_token(user)}
    return {"message":"Login failed"}