from repositories.db import Base
from sqlalchemy import Column, Integer, ForeignKeyConstraint, String
from sqlalchemy.orm import relationship


class ShipCoordinates(Base):
    __tablename__ = "ship_coordinates"
    id = Column(Integer, primary_key=True)
    ship_id = Column(Integer, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    vector = Column(String, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['ship_id'], ['ships.ship_id'],
            ondelete='CASCADE'
        ),
    )

    ship = relationship("Ship", back_populates="ship_coordinates")

    def __init__(self, ship_id: int, x: int, y: int, time: int, speed: int, vector: str):
        self.ship_id = ship_id
        self.x = x
        self.y = y
        self.time = time
        self.speed = speed
        self.vector = vector
