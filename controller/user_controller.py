from fastapi import Query, Request

from main import app
from model.user_model import UserModel, User

obj = UserModel()


@app.get('/')
def hello_world():
    return "hello world!"


@app.get('/api/users')
def all_users(email: str = Query(default=None), ip_register: str = Query(default=None)):
    return obj.get_users(email, ip_register)


@app.post("/api/users")
def add_user(data: User):
    return obj.add_user_model(data)


@app.delete("/api/users/{uid}")
def delete_user(uid: int):
    return obj.delete_user_model(uid)


@app.put("/api/users/{uid}")
async def update_user(request: Request):
    form_data = await request.form()
    return obj.update_user_model(form_data)


@app.patch("/api/users/{uid}")
async def update_user(uid: int, request: Request):
    form_data = await request.form()
    return obj.patch_user_model(form_data, uid)
