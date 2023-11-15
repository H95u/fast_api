from fastapi import Query, Request, APIRouter
from model.add_sukien_model import Add_Sukien_Model

router = APIRouter()
obj = Add_Sukien_Model()


@router.get("/api/add-sukiens")
def get_add_sukiens():
    return obj.get_add_sukiens()


@router.delete("/api/add-sukiens/{sid}")
def delete_add_sukiens(sid: int):
    return obj.delete_add_sukien(sid)