from httpx import AsyncClient


class ApiDAO:
    ...
    # @classmethod
    # async def get_api_by_id(cls, api_id: int):
    #     async with AsyncClient() as client:
    #         response = await client.get(f"https://url/api/v1/api/{api_id}")
    #         return response.json()
