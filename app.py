from fastapi import FastAPI
from requests import get
from random import choice


app = FastAPI()


@app.get("/random")
async def random(favgroup: str = "37193"):
    posts = []
    page = 0
    while len(posts) % 50 == 0:
        page += 1
        posts += get(f"https://danbooru.donmai.us/posts.json?tags=favgroup%3A{favgroup}&limit=50&page={page}").json()
    return get(f'https://danbooru.donmai.us/posts/{choice(posts).get("id")}.json').json().get("file_url")
