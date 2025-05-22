from fastapi import status

from app.exceptions.base import BaseHTTPException


class UserAlreadyExistsExc(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Such a user already exists"


class UserNotYetRegisteredExc(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "User not yet registered"


class UserNotFoundExc(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"


class UserIsAlreadyRegisteredExc(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User is already registered"


class UserPhoneIsExistsExc(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Number is registered"


class UserValidateTelegramIDExc(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "The telegram_id field must be 9 characters long"


class UserValidateNameExc(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Name length error"


class UserValidateSurNameExc(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Surname length error"


class UserValidateLastNameExc(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Lastname length error"


class UserValidateCountryExc(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Country length error"


class UserValidateTownExc(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Town length error"


class UserTelegramIDNotEqualExc(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Telegram ids are different"


class UserAuthorizationIsMissingExc(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Missing authorization header"


class UserInvalidHeaderFormatExc(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Authorization invalid header format"


class UserPhoneValidateExc(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Incorrect phone number format"


class UserPhoneSymbolsValidateExc(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "The phone number should contain only numbers and a '+' sign at the beginning"


class UserVerifyNumberFalseExc(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Phone number has not been confirmed"


class UserEmailFalseExc(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Email not confirmed"


class UserVerifyNumberFalseLoginExc(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Phone has not been confirmed"


class TokenNotFoundExc(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token not found"


class TokenExpiredExc(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token has expired"


class IncorrectTokenFormatExc(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid token format"


class UserIsNotPresentExc(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Not authorized"


class UserEntryStatusTrueExc(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "The entry has already been completed"


class UserEntryStatusFalseExc(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "The user has not logged in yet"


class UserPhoneExistsExc(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Is registered"


class CaseNotFoundExc(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Case not found"


class IncorrectEmailOrPasswordException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"


class InvalidTokenExc(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid token"