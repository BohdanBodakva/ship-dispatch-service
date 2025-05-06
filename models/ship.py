from repositories.db import Base
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship


class Ship(Base):
    __tablename__ = "ships"
    id = Column(Integer, primary_key=True)
    ship_id = Column(Integer, unique=True)

    ship_coordinates = relationship("ShipCoordinates", back_populates="ship", cascade="all, delete-orphan")

    def __init__(self, ship_id: int):
        self.ship_id = ship_id
