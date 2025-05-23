from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse

from app.abstractions.unitofwork import UnitOfWork
from app.dependencies.unitofwork import UOWDep
from app.dependencies.users import get_current_user
from app.models.users import User
from app.schemas.exceptions import SuccessResponse
from app.schemas.users import SUserCreate, SUserCurrent, SUserLogin, SUserTokens
from app.services.passes import PassesService
from app.services.users import UsersService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", summary="Регистрация пользователя", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: SUserCreate, uow: UOWDep, response: Response) -> SUserCurrent:
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


@router.post("/refresh", summary="Обновить access_token", status_code=status.HTTP_200_OK)
async def refresh_token(uow: UOWDep, response: Response, request: Request) -> SUserTokens:
    """
    **Обновить access_token**
    """
    tokens = await UsersService().refresh_token(uow, response, request)
    return tokens


@router.post("/logout", summary="Закончить сессию у пользователя", status_code=status.HTTP_200_OK)
async def logout(
    uow: UOWDep, response: Response, request: Request, user: User = Depends(get_current_user)
) -> SuccessResponse:
    """
    **Закончить сессию у пользователя**
    """
    await UsersService().logout(uow, response, request)
    return {"statusCode": 200, "message": "Success. Logout"}



@router.post("/alice-webhook")
async def webhook(request: Request):
    body = await request.json()
    print("Запрос от Алисы:", body)

    session_is_new = body["session"]["new"]

    if session_is_new:
        response = {
            "response": {
                "text": "Кого нужно зарегистрировать? Пожалуйста, скажите фамилию, имя и отчество.",
                "end_session": False
            },
            "session": body["session"],
            "version": body["version"]
        }
        return JSONResponse(status_code=200, content=response)

    try:
        fio = body['request']['original_utterance'].strip()

        if not fio:
            raise ValueError("ФИО не распознано")

        uow = UnitOfWork()
        await PassesService().create_pass_with_alice(uow, fio)

        response_text = f"Заявка на {fio} успешно создана!"
        response = {
            "response": {
                "text": response_text,
                "end_session": True
            },
            "session": body["session"],
            "version": body["version"]
        }
        return JSONResponse(status_code=200, content=response)
    except ValueError:
        response_text = "Я не расслышала ФИО. Пожалуйста, повторите еще раз."

        response = {
            "response": {
                "text": response_text,
                "end_session": False
            },
            "session": body["session"],
            "version": body["version"]
        }
    except Exception as e:
        print("Ошибка при обработке запроса:", e)
        response_text = "Пользователь не найден или ошибка в ФИО"

    response = {
        "response": {
            "text": response_text,
            "end_session": True
        },
        "session": body["session"],
        "version": body["version"]
    }

    return JSONResponse(status_code=200, content=response)
