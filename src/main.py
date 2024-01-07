import asyncio

from sqlalchemy.orm import sessionmaker

from scripts.building import fetch_building_list, insert_building
from scripts.map import fetch_campus
from scripts.room import fetch_room_list, insert_room
from utils.database import get_db_engine


def main():
    buildings = asyncio.run(fetch_campus())
    building_posts = asyncio.run(fetch_building_list(buildings))
    rooms = asyncio.run(fetch_room_list(building_posts))
    # Insert data into database
    connection = get_db_engine()
    session_constructor = sessionmaker(bind=connection)
    session = session_constructor()
    if session is None:
        raise RuntimeError("Failed to get db session")
    asyncio.run(insert_building(session, building_posts))
    asyncio.run(insert_room(session, rooms))
    session.commit()
    session.close()
    connection.dispose()


if __name__ == "__main__":
    main()
