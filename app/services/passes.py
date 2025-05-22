from app.abstractions.unitofwork import UnitOfWork
from app.models.passes import Passes
from app.models.users import User
from app.schemas.passes import PassCreate


class PassesService:
    
    async def create_pass(self, uow: UnitOfWork, pass_data: PassCreate, user: User) -> Passes:
        async with uow:
            new_pass = await uow.passes.insert_by_data(
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
                    "user_id": user.id
                }
            )
            await uow.passes.create_ujin_pass(pass_data=pass_data, user=user)
            uow.session.expunge(new_pass)
            return new_pass