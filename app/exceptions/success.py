from fastapi import status

from app.exceptions.base import BaseHTTPException


class SuccessException(BaseHTTPException):
    def __init__(self, detail: str):
        super().__init__()
        self.status_code = status.HTTP_200_OK
        self.detail = detail
