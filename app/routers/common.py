import httpx

API_KEY = "D805IVKWUQK24V45"


async def call(URL: str):
    response = await httpx.AsyncClient().get(URL + f"&apikey={API_KEY}")
    return response.text
