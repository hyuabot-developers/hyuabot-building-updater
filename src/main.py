import asyncio

from scripts.building import fetch_building_list
from scripts.map import fetch_campus
from scripts.room import fetch_room_list

if __name__ == "__main__":
    buildings = asyncio.run(fetch_campus())
    building_posts = asyncio.run(fetch_building_list(buildings))
    rooms = asyncio.run(fetch_room_list(building_posts))
