from fastapi import APIRouter

from forum.features.reply.dependencies import ReplyServiceDep
from forum.features.reply.schemas import ReplyCreateDTO, ReplyDTO
from forum.features.user.dependencies import CurrentUserDep

router = APIRouter(prefix="/replies", tags=["Replies"])


@router.put("/", response_model=ReplyDTO, status_code=201)
async def create_reply(
    reply: ReplyCreateDTO,
    current_user: CurrentUserDep,
    reply_service: ReplyServiceDep,
) -> ReplyDTO:
    return reply_service.create_reply(current_user, reply)
