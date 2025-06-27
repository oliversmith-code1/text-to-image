from pydantic import BaseModel

class GenerateRequest(BaseModel):
    text: str

class GenerateResponse(BaseModel):
    url: str
