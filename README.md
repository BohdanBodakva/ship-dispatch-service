# Ship Dispatch Service

Service, that imitates a ship dispatch service, where ships can send their coordinates at the moment of time, and service is available to rate possible ships collisions to determine zone where ships are located: "green" (collisions are impossible), "yellow" (ships run in 1 distance unit from each other), "red" (collision is expected).


## How to run
1. Execute command in terminal to clone the repository:
"git clone -b master https://github.com/BohdanBodakva/ship-dispatch-service.git"
2. Navigate to firectory you've just cloned
3. Start Docker client (Docker Desktop)
4. Execute command to run docker-compose:
"docker-compose up --build"
5. Open browser/Postman and try to execute GET request to "http://localhost:8000/v1/api/ships" address
6. If you see "{"ships":[]}" as response, it means everything is working!

## How to use
1. POST /v1/api/ships/:id/position (body: {“time: 1744383218, “x”: 2, “y”: 3})
Send ship cooordinates at the moment of time
2. GET /v1/api/ships
Get all ships' last coordinates and zones
3. GET /v1/api/ships/:id
Get special ship history (coordinates, time and speed)
4. POST /v1/api/flush
Clears all ships/coordinates data from database 

## Implementation details
The application is written with FastAPI framework and contains three-layer architecture (router-service-repository). Service layer is one where main calculations are done. 
There are two db models in the architecture: Ship (storing just ship ids) and ShipCoordinates (storing coordinates(x, y), time). When ship send its coordinates its current speed and move vector are calculated immediately and written to db (in ShipCoordinates model).
Zone is caclulated every time we execute request (because ships can send location with different time frequency, so it may affect all ships' zones every time moment).
