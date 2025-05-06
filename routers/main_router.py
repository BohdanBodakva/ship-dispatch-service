from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from repositories.db import get_db
from services.dispatch_service import DispatchService

ship_router = APIRouter()

db_gen = get_db()
dispatch_service = DispatchService()


@ship_router.get("/ships")
def get_all_ships_info():
    try:
        result = dispatch_service.get_ships_info()
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


@ship_router.get("/ships/{ship_id}")
def get_ship_info(ship_id: int):
    try:
        result = dispatch_service.get_ship_history(ship_id)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


@ship_router.post("/ships/{ship_id}/position")
async def place_ship(ship_id: int, request: Request):
    try:
        body = await request.json()
        time = body.get("time")
        x = body.get("x")
        y = body.get("y")

        if time and x and y:
            try:
                coordinates = dispatch_service.ship_coordinates_repo.create(ship_id, x, y, time)
            except Exception as e:
                return JSONResponse(content={"error": "time out of range"}, status_code=422)

            _, zones = dispatch_service.get_ships_coordinates_and_zones()
            zone = zones[ship_id]

            return JSONResponse(content={
                "time": coordinates.time,
                "x": coordinates.x,
                "y": coordinates.y,
                "speed": coordinates.speed,
                "status": zone
            }, status_code=201)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


@ship_router.post("/flush")
def clear_all_data():
    try:
        dispatch_service.ship_repo.delete_all()
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
