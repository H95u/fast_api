from fastapi import Query, Request, APIRouter

from model.message_model import MessageModel

router = APIRouter()
obj = MessageModel()


@router.get("/api/messages")
def get_messages(id_user: int = Query()):
    return obj.get_user_contact_history(id_user)
