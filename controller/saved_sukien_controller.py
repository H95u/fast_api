from fastapi import Query, Request, APIRouter
from model.saved_sukien_model import Saved_Sukien_Model

router = APIRouter()
obj = Saved_Sukien_Model()


@router.get("/api/saved-sukiens")
def get_saved_sukiens():
    return obj.get_saved_sukiens()


@router.delete("/api/saved-sukiens/{cid}")
def get_saved_sukiens(cid: int):
    return obj.delete_saved_sukien(cid)
