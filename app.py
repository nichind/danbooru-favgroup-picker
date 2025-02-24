from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from aiohttp import ClientSession
import asyncio
from random import choice


app = FastAPI()


async def get_json(url: str, session: ClientSession):
    async with session.get(url) as response:
        return await response.json()


@app.get("/random")
async def random(favgroup: str = "37191", asImg: bool = True, startPage: int = 1):
    try:
        posts = []
        page = startPage - 1
        async with ClientSession() as session:
            while len(posts) % 100 == 0:
                page += 1
                posts += await get_json(f"https://danbooru.donmai.us/posts.json?tags=favgroup%3A{favgroup}&limit=100&page={page}", session)
                if len(posts) >= 200:
                    break
            file_url = (await get_json(f'https://danbooru.donmai.us/posts/{choice(posts).get("id")}.json', session)).get("file_url")
            if not asImg:
                return RedirectResponse(file_url)
            async with session.get(file_url) as resp:
                return Response(content=await resp.content.read(), media_type="image/png")
    except Exception as e:
        return 'bruh exception bro'

