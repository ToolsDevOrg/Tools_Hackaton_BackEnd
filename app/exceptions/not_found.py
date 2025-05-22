from fastapi import status

from app.exceptions.base import BaseHTTPException


class NotFoundException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found"
