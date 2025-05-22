from pydantic import BaseModel


class SuccessResponse(BaseModel):
    statusCode: int = 200
    message: str
