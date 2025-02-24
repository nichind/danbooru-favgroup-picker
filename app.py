from fastapi import FastAPI, Response
from requests import get
from random import choice


app = FastAPI()


@app.get("/random")
async def random(favgroup: str = "37193", asImg: bool = True):
    posts = []
    page = 0
    while len(posts) % 50 == 0:
        page += 1
        posts += get(f"https://danbooru.donmai.us/posts.json?tags=favgroup%3A{favgroup}&limit=50&page={page}").json()
    file_url = get(f'https://danbooru.donmai.us/posts/{choice(posts).get("id")}.json').json().get("file_url")
    if not asImg:
        return file_url
    return Response(get(file_url).content)
