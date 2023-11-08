from fastapi import Query, Request, APIRouter
from model.saved_sukien_model import Saved_Sukien_Model

router = APIRouter()
obj = Saved_Sukien_Model()


@router.get("/api/saved-sukiens")
def get_saved_sukiens():
    return obj.get_saved_sukiens()


@router.delete("/api/saved-sukiens/{eid}")
def delete_saved_sukiens(eid: int):
    return obj.delete_saved_sukien(eid)


@router.patch("/api/saved-sukiens/{eid}")
async def patch_saved_sukiens(eid: int, request: Request):
    form_data = await request.form()
    return obj.patch_saved_sukien(eid, form_data)
