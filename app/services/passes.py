from datetime import datetime
import uuid

from app.abstractions.unitofwork import UnitOfWork
from app.exceptions.passes.exceptions import PassNotFoundExc
from app.exceptions.users.exceptions import UserNotFoundExc
from app.models.enums import PassTypeEnum
from app.models.passes import Passes
from app.models.users import User
from app.schemas.passes import SPassCreate


class PassesService:

    async def create_pass(self, uow: UnitOfWork, pass_data: SPassCreate, user: User) -> Passes:
        async with uow:
            new_pass: Passes = await uow.passes.insert_by_data(
                {
                    "title": pass_data.title,
                    "start_date": pass_data.start_date,
                    "location": pass_data.location,
                    "latitude": pass_data.latitude,
                    "longitude": pass_data.longitude,
                    "policy_area": pass_data.policy_area,
                    "organizer": pass_data.organizer,
                    "participants": pass_data.participants,
                    "pass_type": pass_data.pass_type,
                    "car_number": pass_data.car_number,
                    "user_id": user.id,
                }
            )
            pass_number = await uow.passes.create_ujin_pass(pass_data=pass_data, user=user)

            await uow.passes.update_by_filter({"pass_number_ujin": int(pass_number)}, id=new_pass.id)

            uow.session.expunge(new_pass)
            await uow.commit()
            return new_pass

    async def get_by_filter(self, uow: UnitOfWork, filter_type: PassTypeEnum, user: User) -> list[Passes]:
        async with uow:
            passes = await uow.passes.find_all_by_filter(user_id=user.id, pass_type=filter_type.value.lower())
            if passes:
                uow.session.expunge_all()
            return passes

    async def get_pass_detail(self, uow: UnitOfWork, pass_id: uuid.UUID, user: User):
        async with uow:
            my_pass = await uow.passes.find_one_or_none(id=pass_id)
            if not my_pass:
                raise PassNotFoundExc
            uow.session.expunge(my_pass)
            return my_pass
        
    async def create_pass_with_alice(self, uow: UnitOfWork, pass_data: str) -> None:
        async with uow:
            formatted_data = pass_data.title()
            find_user: User | None = await uow.users.find_one_or_none(fio=formatted_data)
            if not find_user:
                raise UserNotFoundExc
            
            new_pass: Passes = await uow.passes.insert_by_data(
                {
                    "title": "title",
                    "start_date": datetime.strptime("2025-05-23", "%Y-%m-%d").date(),
                    "location": "location",
                    "latitude": 0,
                    "longitude": 0,
                    "policy_area": "policy_area",
                    "organizer": "organizer",
                    "participants": 100,
                    "pass_type": "event",
                    "car_number": None,
                    "user_id": find_user.id,
                }
            )
            # pass_number = await uow.passes.create_ujin_pass_with_alice(pass_data=pass_data)

            # await uow.passes.update_by_filter({"pass_number_ujin": int(pass_number)}, id=new_pass.id)
            
            uow.session.expunge(new_pass)
            await uow.commit()
            
                
