from fastapi import APIRouter, Depends
from app.dependencies.unitofwork import UOWDep
from app.models.users import User
from app.api.users import get_current_user
from app.schemas.passes import PassCreate
from app.services.passes import PassesService

router = APIRouter(prefix="/passes", tags=["Passes"])

@router.post("/create", status_code=200, summary="Создать пропуск")
async def create_pass(uow: UOWDep, pass_data: PassCreate, user: User = Depends(get_current_user)):
    """
    **Создать пропуск
    
    `pass_type` - _car_ - автомобиль, _event_ - мероприятие
    """
    new_pass = await PassesService().create_pass(uow, pass_data, user)
    return new_pass



