from fastapi import Query, Request, APIRouter
from model.auth_model import Auth_Model

router = APIRouter()
obj = Auth_Model()


@router.post("/api/users/change-password/{uid}")
async def change_user_password(uid: int, request: Request):
    form_data = await request.form()
    return obj.change_user_password(form_data, uid)


@router.post("/api/users/login")
async def change_user_password(request: Request):
    form_data = await request.form()
    return obj.login_user(form_data)