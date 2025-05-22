import enum

from sqlalchemy import Enum


class UserRoleEnum(str, enum.Enum):
    CITIZEN = "citizen"
    EMPLOYEE = "employee"


class PassTypeEnum(str, enum.Enum):
    CAR = "car"
    EVENT = "event"


class PassStatusEnum(str, enum.Enum):
    CONFIRMED = "confirmed"
    UNCONFIRMED = "unconfirmed"


user_role_enum = Enum(UserRoleEnum, name="user_role_enum")
pass_type_enum = Enum(PassTypeEnum, name="pass_type_enum")
pass_status_enum = Enum(PassStatusEnum, name="pass_status_enum")
