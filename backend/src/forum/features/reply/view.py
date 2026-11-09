from typing import Annotated

from fastapi import APIRouter, Depends

from forum.features.reply.dependencies import ReplyServiceDep
from forum.features.reply.schemas import ReplyCreateDTO, ReplyDTO
from forum.features.user.database.models import User
from forum.features.user.session import get_current_user

router = APIRouter(prefix="/replies", tags=["Replies"])


@router.put("/", response_model=ReplyDTO, status_code=201)
async def create_reply(
    reply: ReplyCreateDTO,
    current_user: Annotated[User, Depends(get_current_user)],
    reply_service: ReplyServiceDep,
) -> ReplyDTO:
    return reply_service.create_reply(current_user, reply)
