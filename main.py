
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from os import environ
from Controllers import User

app = FastAPI()
allowed_origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(User.router, prefix="/user", tags=["user"])


@app.get("/")
async def root():
    return {"message": "Hello World"}




