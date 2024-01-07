import asyncio
from typing import Optional

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from models import BaseModel, Building, Room
from scripts.building import fetch_building_list, insert_building
from scripts.map import fetch_campus
from scripts.room import fetch_room_list, insert_room
from tests.insert_campus_data import insert_campus_data
from utils.database import get_db_engine


class TestFetchRealtimeData:
    connection: Optional[Engine] = None
    session_constructor = None
    session: Optional[Session] = None

    @classmethod
    def setup_class(cls):
        cls.connection = get_db_engine()
        cls.session_constructor = sessionmaker(bind=cls.connection)
        # Database session check
        cls.session = cls.session_constructor()
        assert cls.session is not None
        # Migration schema check
        BaseModel.metadata.create_all(cls.connection)
        # Insert initial data
        asyncio.run(insert_campus_data(cls.session))
        cls.session.commit()
        cls.session.close()

    @pytest.mark.asyncio
    async def test_fetch_building_data(self):
        buildings = await fetch_campus()
        building_posts = await fetch_building_list(buildings)
        rooms = await fetch_room_list(building_posts)
        # Insert data into database
        connection = get_db_engine()
        session_constructor = sessionmaker(bind=connection)
        session = session_constructor()
        if session is None:
            raise RuntimeError("Failed to get db session")
        await insert_building(session, building_posts)
        await insert_room(session, rooms)
        session.commit()
        session.close()
        connection.dispose()

        # Check if the data is inserted
        building_list = session.query(Building).all()
        assert len(building_list) > 0
        for building in building_list:
            assert building.name is not None
            assert building.campus_id is not None
            assert building.latitude is not None
            assert building.longitude is not None
        room_list = session.query(Room).all()
        assert len(room_list) > 0
        for room in room_list:
            assert room.building is not None
            assert room.name is not None
            assert room.number is not None
