from fastapi import status

from app.exceptions.base import BaseHTTPException


class PassNotFoundExc(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Pass not found"
    
class RequiredCarNumberExc(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Car number required"