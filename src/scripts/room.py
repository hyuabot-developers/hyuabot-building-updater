import asyncio

import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy import delete, insert
from sqlalchemy.orm import Session

from models import Room


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
        floor_list = soup.select("div > div > div > table > tbody")
        for floor in floor_list:
            room_list = floor.select("tr > td")
            for room in room_list:
                data = room.text.strip()
                raw_data.append(data)
    for index in range(0, len(raw_data) - 1, 2):
        if raw_data[index] is None or raw_data[index] == "​" or len(raw_data[index].strip()) == 0:
            continue
        elif raw_data[index + 1] is None or raw_data[index + 1] == "​" or len(raw_data[index + 1].strip()) == 0:
            continue
        room_data.append({"building": name, "number": raw_data[index], "name": raw_data[index + 1]})
    return room_data


async def insert_room(db_session: Session, data: list[dict]):
    delete_statement = delete(Room)
    db_session.execute(delete_statement)
    mapped_data = list(map(lambda x: {
        "building": x.get("building"),
        "number": x.get("number"),
        "name": x.get("name"),
    }, data))
    db_session.execute(
        insert(Room),
        mapped_data,
    )
