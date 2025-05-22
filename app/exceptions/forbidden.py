from fastapi import status

from app.exceptions.base import BaseHTTPException


class ForBiddenException(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Resource forbidden"


class PermissionAccessDenied(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Permission access denied"


class AccessDenied(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Access denied"
