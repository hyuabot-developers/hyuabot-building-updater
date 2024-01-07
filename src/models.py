from sqlalchemy import String, Integer, Float, Text, PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    pass


class Campus(BaseModel):
    __tablename__ = "campus"
    campus_id: Mapped[int] = mapped_column(primary_key=True)
    campus_name: Mapped[str] = mapped_column(nullable=False)


class Building(BaseModel):
    __tablename__ = "building"
    name: Mapped[str] = mapped_column("name", String(30), primary_key=True)
    building_id: Mapped[str] = mapped_column("id", String(15))
    campus_id: Mapped[str] = mapped_column("campus_id", Integer)
    latitude: Mapped[float] = mapped_column("latitude", Float)
    longitude: Mapped[float] = mapped_column("longitude", Float)
    link: Mapped[str] = mapped_column("url", Text, nullable=True)


class Room(BaseModel):
    __tablename__ = "room"
    __table_args__ = (PrimaryKeyConstraint("building_name", "number"),)
    building: Mapped[str] = mapped_column("building_name", String(30))
    name: Mapped[str] = mapped_column("name", String(100))
    number: Mapped[str] = mapped_column("number", String(30))
