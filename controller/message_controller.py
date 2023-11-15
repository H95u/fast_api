from fastapi import Query, Request, APIRouter

from model.message_model import MessageModel

router = APIRouter()
obj = MessageModel()


@router.get("/api/messages")
def get_messages(id_user: int = Query()):
    return obj.get_messages_by_id_user(id_user)
