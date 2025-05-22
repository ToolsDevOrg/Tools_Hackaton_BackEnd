from fastapi import status

from app.exceptions.base import BaseHTTPException


class CreatedException(BaseHTTPException):
    status_code = status.HTTP_201_CREATED
    detail = "Success. Created"
