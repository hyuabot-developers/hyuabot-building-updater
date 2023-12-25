import asyncio

from scripts.building import fetch_building_list

if __name__ == "__main__":
    buildings = asyncio.run(fetch_building_list())
