import asyncio

import aiohttp
from bs4 import BeautifulSoup


async def fetch_room_list(building_posts: list[dict]) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for building_post in building_posts:
            if building_post.get("link"):
                tasks.append(asyncio.create_task(
                    fetch_room_page(session, building_post.get("name"), building_post.get("link"))))
        values = await asyncio.gather(*tasks)
    room_list = []
    for value in values:
        room_list.extend(value)
    return room_list


async def fetch_room_page(session, name, url) -> list[dict]:
    room_data = []
    async with session.get(url) as response:
        raw_data = []
        response_text = await response.text()
        soup = BeautifulSoup(response_text, "html.parser")
        room_list = soup.select("div > div > div > table > tbody > tr > td")
        for room in room_list:
            data = room.text.strip()
            if data and data != "\u200b":
                raw_data.append(data)
    for index in range(0, len(raw_data) - 1, 2):
        room_data.append({"building": name, "number": raw_data[index], "name": raw_data[index + 1]})
    return room_data
