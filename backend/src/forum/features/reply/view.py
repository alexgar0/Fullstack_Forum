from fastapi import APIRouter, Depends
from forum.features.query import PaginationQuery
from forum.features.reply.database.service import ReplyService, get_reply_service
from forum.features.reply.schemas import ReplyCreateDTO, ReplyDTO
from forum.features.user.database.models import User
from forum.features.user.session import get_current_user


router = APIRouter(prefix="/replies", tags=["Replies"])

@router.put("/", response_model=ReplyDTO, status_code=201)
async def create_reply(
    reply: ReplyCreateDTO,
    current_user: User = Depends(get_current_user),
    reply_service: ReplyService = Depends(get_reply_service),
) -> ReplyDTO:
    new_reply = reply_service.create_reply(current_user, reply)
    return new_reply