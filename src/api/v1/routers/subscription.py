from fastapi import APIRouter, Depends, HTTPException, status

from src.api.v1.schemas.subscription import SubscriptionSchema
from src.bot.subs import join_chat
router = APIRouter()


@router.post('/subscription',
             status_code=status.HTTP_204_NO_CONTENT,
             description=(
                 "Subscribes bot to a given channel\n\n"
                 "Respond 400 for any exceptions"
             ),
             )
async def create_subscription(request: SubscriptionSchema):
    link = request.link
    success, error = await join_chat(link)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

