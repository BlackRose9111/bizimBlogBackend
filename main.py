import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Controllers import User,Authentication,blog,Category

app = FastAPI()


allowed_origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(User.router, prefix="/user", tags=["user"])
app.include_router(blog.router, prefix="/blog", tags=["blog"])
app.include_router(Authentication.router, prefix="/auth", tags=["auth"])
app.include_router(Category.router, prefix="/categories", tags=["categories"])



@app.get("/")
async def root():
    return {"message": "Hello World"}




