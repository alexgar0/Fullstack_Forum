from typing import Annotated

from fastapi import Depends

from forum.features.reply.service import ReplyService, get_reply_service

ReplyServiceDep = Annotated[ReplyService, Depends(get_reply_service)]
