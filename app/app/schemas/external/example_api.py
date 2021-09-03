from pydantic import BaseModel


class StatusCheck(BaseModel):
    value: str
