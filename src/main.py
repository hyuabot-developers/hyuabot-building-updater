import asyncio

from scripts.building import fetch_building_list
from scripts.room import fetch_room_list

if __name__ == "__main__":
    buildings = asyncio.run(fetch_building_list())
    rooms = asyncio.run(fetch_room_list(buildings))
