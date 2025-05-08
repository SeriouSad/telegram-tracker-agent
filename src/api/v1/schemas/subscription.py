from pydantic import BaseModel


class SubscriptionSchema(BaseModel):
    link: str
