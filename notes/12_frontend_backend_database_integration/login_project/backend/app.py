# uvicorn app:app --reload
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crud import login_, register_, clock_out_

class User(BaseModel):
    email: str
    password: str

class ClockOut(BaseModel):
    email: str
    clock_in: str
    clock_out: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
def login(user: User):
    success = login_(user.email, user.password)
    return {"success": success}

@app.post("/register")
def register(user: User):
    if user.email == "" or user.password == "":
        return {"success": False}

    success = register_(user.email,user.password)
    return {"success": success}

@app.post("/clockout")
def clockout(data: ClockOut):
    clock_out_(data.email, data.clock_in, data.clock_out)
    return { "success": True}