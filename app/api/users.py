from fastapi import APIRouter, Depends, Request, status, Response
from app.dependencies.unitofwork import UOWDep
from app.dependencies.users import get_current_user
from app.models.users import User
from app.schemas.exceptions import SuccessResponse
from app.schemas.users import SUserCurrent, SUserCreate, SUserLogin, SUserTokens
from app.services.users import UsersService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post(
    "/register",
    summary="Регистрация пользователя",
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: SUserCreate,
    uow: UOWDep,
    response: Response
) -> SUserCurrent:
    """
    **Регистрация пользователя**
    
    `role` - _citizen_ - житель, _employee_ - сотрудник
    """
    new_user = await UsersService().register_user(uow, user_data, response)
    return new_user


@router.post("/login", summary="Вход пользователя", status_code=status.HTTP_200_OK)
async def login(uow: UOWDep, user_data: SUserLogin, response: Response) -> SUserCurrent:
    """**Вход пользователя**"""
    login_data = await UsersService().login(uow, user_data, response)
    return login_data

@router.get("/current", summary="Текущий пользователь", status_code=status.HTTP_200_OK)
async def get_current_user(user: User = Depends(get_current_user)) -> SUserCurrent:
    """**Текущий пользователь**"""
    return user


@router.post(
    "/refresh",
    summary="Обновить access_token",
    status_code=status.HTTP_200_OK
)
async def refresh_token(uow: UOWDep, response: Response, request: Request) -> SUserTokens:
    """
    **Обновить access_token**
    """
    tokens = await UsersService().refresh_token(uow, response, request)
    return tokens


@router.post(
    "/logout",
    summary="Закончить сессию у пользователя",
    status_code=status.HTTP_200_OK
)
async def logout(uow: UOWDep, response: Response, request: Request, user: User = Depends(get_current_user)) -> SuccessResponse:
    """
    **Закончить сессию у пользователя**
    """
    await UsersService().logout(uow, response, request)
    return {"statusCode": 200, "message": "Success. Logout"}

