from fastapi import status

from app.exceptions.base import BaseHTTPException


class TooManyRequestsExc(BaseHTTPException):
    def __init__(self, detail: str):
        super().__init__()
        self.status_code = status.HTTP_429_TOO_MANY_REQUESTS
        self.detail = detail
