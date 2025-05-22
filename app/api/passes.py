import uuid
from fastapi import APIRouter, Depends
from app.dependencies.unitofwork import UOWDep
from app.models.enums import PassTypeEnum
from app.models.users import User
from app.api.users import get_current_user
from app.schemas.passes import SPassCreate, SPassCurrent
from app.services.passes import PassesService

router = APIRouter(prefix="/passes", tags=["Passes"])

@router.post("/create", status_code=200, summary="Создать пропуск")
async def create_pass(uow: UOWDep, pass_data: SPassCreate, user: User = Depends(get_current_user)) -> SPassCurrent:
    """
    **Создать пропуск
    
    `pass_type` - _car_ - автомобиль, _event_ - мероприятие
    """
    new_pass = await PassesService().create_pass(uow, pass_data, user)
    return new_pass


@router.get("/detail/{pass_id}", status_code=200, summary="Рассмотреть детально пропуск")
async def get_pass_detail(uow: UOWDep, pass_id: uuid.UUID, user: User = Depends(get_current_user)) -> SPassCurrent:
    my_pass = await PassesService().get_pass_detail(uow, pass_id, user)
    return my_pass


@router.get("/filer/{filter_type}", status_code=200, summary="Получить пропуска по фильтру")
async def get_by_filter(uow: UOWDep, filter_type: PassTypeEnum, user: User = Depends(get_current_user)) -> list[SPassCurrent]:
    passes = await PassesService().get_by_filter(uow, filter_type, user)
    return passes



