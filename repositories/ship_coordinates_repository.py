import math
from datetime import datetime

from handlers.unix_timestamp_converter import TimestampConverter
from models.ship_coordinates import ShipCoordinates
from repositories.db import SessionLocal
from repositories.ship_repository import ShipRepository


class ShipCoordinatesRepository:
    def __init__(self):
        self.ship_repo = ShipRepository()

    def _verify_coordinates(self, x: int, y: int):
        return not (x == 0 and y == 0)

    def _verify_time(self, ship_id: int, time: int):
        now_time = datetime.now()
        now_unix_time = TimestampConverter.to_timestamp(now_time)

        ship_coordinates = self.get_all_by_ship_id(ship_id)
        if len(ship_coordinates) == 0:
            return time <= now_unix_time, None, now_unix_time

        last_coordinates = max(ship_coordinates, key=lambda s: s.time)
        last_unix_time = last_coordinates.time

        return last_unix_time < time <= now_unix_time, last_unix_time, now_unix_time

    def _calculate_speed_and_vector(self, x1: float, y1: float, time1: int,
                                   x2: float, y2: float, time2: int):
        distance = math.hypot(x2 - x1, y2 - y1)

        time_diff = time2 - time1
        if time_diff <= 0:
            raise ValueError("Time difference cannot be zero or less")

        speed = int(distance / time_diff)

        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) > abs(dy):
            vector = 'right' if dx > 0 else 'left'
        else:
            vector = 'top' if dy > 0 else 'bottom'

        return speed, vector

    def create(self, ship_id: int, x: int, y: int, time: int):
        if not self._verify_coordinates(x, y):
            raise ValueError("Ship cannot be placed at coordinates (0;0)")

        time_verified, last_unix_time, now_unix_time = self._verify_time(ship_id, time)
        if not time_verified:
            raise ValueError(
                f"Time must be from '{TimestampConverter.to_human_date(last_unix_time)}' "
                f"to '{TimestampConverter.to_human_date(now_unix_time)}'"
            )

        ship = self.ship_repo.get_by_id(ship_id)
        speed = 0
        vector = "top"
        if not ship:
            ship = self.ship_repo.create(ship_id)
        else:
            prev_coordinates = self.get_ship_last_coordinates(ship_id)
            speed, vector = self._calculate_speed_and_vector(
                prev_coordinates.x, prev_coordinates.y, prev_coordinates.time,
                x, y, time
            )

        coordinates = ShipCoordinates(ship.ship_id, x, y, time, speed, vector)

        session = SessionLocal()
        try:
            session.add(coordinates)
            session.commit()
            session.refresh(coordinates)
        finally:
            session.close()

        return coordinates

    def get_ship_last_coordinates(self, ship_id: int):
        session = SessionLocal()
        try:
            result = session.query(ShipCoordinates).filter(ShipCoordinates.ship_id == ship_id)\
                .order_by(ShipCoordinates.id.desc()).first()
        finally:
            session.close()

        return result

    def get_by_id(self, id: int):
        session = SessionLocal()
        try:
            result = session.query(ShipCoordinates).filter(ShipCoordinates.id == id).first()
        finally:
            session.close()

        return result

    def get_all(self):
        session = SessionLocal()
        try:
            result = session.query(ShipCoordinates).all()
        finally:
            session.close()

        return result

    def get_all_by_ship_id(self, ship_id):
        session = SessionLocal()
        try:
            result = session.query(ShipCoordinates).filter(ShipCoordinates.ship_id == ship_id)\
                .order_by(ShipCoordinates.id.asc()).all()
        finally:
            session.close()

        return result

    def delete_all(self):
        session = SessionLocal()
        try:
            session.query(ShipCoordinates).delete()
            session.commit()
        finally:
            session.close()

        return True
