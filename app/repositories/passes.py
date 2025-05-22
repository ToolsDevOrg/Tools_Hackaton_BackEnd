from datetime import datetime
from app.models.passes import Passes
from app.models.users import User
from app.repositories.base import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from app.config.main import settings
from dateutil.parser import parse

from app.schemas.passes import PassCreate

class PassesRepository(SQLAlchemyRepository):
    model = Passes

    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    async def create_ujin_pass(self, pass_data: PassCreate, user: User) -> None:
        url = (
            "https://api-uae-test.ujin.tech/api/v1/scud/pass/create/"
            f"?token={settings.UJIN_TOKEN}"
            "&egt=6"
            "&eg=b39caef6-0b73-4ae9-ad0b-af6c6ab74bcd"
        )

        headers = {
            "Content-Type": "application/json",
            "Cookie": (
                "PHPSESSID=sr0abp1nh0nh1n17apb29nrtp3; "
                "mysmartflatcook=qzjycwsvrxvwvihfvutpdkzajlacblidrvwyquzshcosjstuivzhmzobntlcgopcshylxmcljocycqnvfsyzchuzurhvjbjdhyxozwcvjacpigrwnvxjuhewfgaobfgklqkvhuazbzuyzvyrjrmkgcrqupilcaolbekvnqsevgflzolahtdzrhyxujvrawgmdkxnjndfihoizrafhejlhypzvszgfpsoikrgngaueokukmrhugcfegluhilkhbsm1"
            ),
        }
        
        formatted_time = pass_data.work_time_from.strftime("%H:%M")

        payload = {
            "user_id": 739698,
            "enterprise_id": 295,
            "work_days": [4, 7],
            "start_date": pass_data.start_date.isoformat(),
            "active_from": pass_data.active_from.isoformat(),
            "work_time_from": formatted_time,
            "work_time_to": "19:00",
            "comment": f"Пропуск на {pass_data.title}, для {user.fio}",
        }

        async with AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            print(f"Status Code pass create: {response.status_code}")
        
        
    