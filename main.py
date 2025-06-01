
from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

with open("users.json", "r") as f:
    USERS = json.load(f)

class UserData(BaseModel):
    username: str
    password: str = ""
    hwid: str
    ip: str = ""

@app.post("/login")
def login(data: UserData):
    user = USERS.get(data.username)
    if not user:
        return {"login_status": False, "message": "user not found"}
    if user["password"] != data.password:
        return {"login_status": False, "message": "wrong password"}
    if user["hwid"] != data.hwid:
        return {"login_status": False, "message": "hwid mismatch"}
    return {"login_status": True, "sub": user.get("sub")}

@app.post("/auto-load")
def auto_load(data: UserData):
    for user in USERS.values():
        if user["hwid"] == data.hwid:
            return {"login_status": True, "sub": user.get("sub")}
    return {"login_status": False, "message": "invalid hwid"}

@app.post("/2fa")
def twofa(data: UserData):
    user = USERS.get(data.username)
    if user and user["hwid"] == data.hwid:
        return {"fa2_status": True}
    return {"fa2_status": False}

@app.get("/get-lua")
def get_lua():
    with open("your_script.lua", "r", encoding="utf-8") as f:
        return f.read()
