from pydantic import BaseModel

class blogRequestBody(BaseModel):
    title: str
    body: str