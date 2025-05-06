from models.ship import Ship
from repositories.db import SessionLocal


class ShipRepository:
    def create(self, ship_id: int):
        session = SessionLocal()
        try:
            ship = Ship(ship_id)
            session.add(ship)
            session.commit()
            session.refresh(ship)
        finally:
            session.close()

        return ship

    def get_by_id(self, ship_id):
        session = SessionLocal()
        try:
            result = session.query(Ship).filter(Ship.ship_id == ship_id).first()
        finally:
            session.close()

        return result

    def get_all(self):
        session = SessionLocal()
        try:
            result = session.query(Ship).all()
        finally:
            session.close()

        return result

    def delete_all(self):
        session = SessionLocal()
        try:
            session.query(Ship).delete()
            session.commit()
        finally:
            session.close()

        return True
