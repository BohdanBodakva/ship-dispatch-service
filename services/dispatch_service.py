from repositories.ship_repository import ShipRepository
from repositories.ship_coordinates_repository import ShipCoordinatesRepository


class DispatchService:
    def __init__(self):
        self.ship_repo = ShipRepository()
        self.ship_coordinates_repo = ShipCoordinatesRepository()

    def get_zone(self, x1, y1, x2, y2):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)

        if dx == 0 and dy == 0:
            return "red"
        elif dx <= 1 and dy <= 1:
            return "yellow"

        return "green"

    def get_trajectory_function(self, x, y, speed, angle, second):
        if angle == "top":
            return x, y + speed * second
        elif angle == "bottom":
            return x, y - speed * second
        elif angle == "left":
            return x - speed * second, y
        elif angle == "right":
            return x + speed * second, y

    def get_zone_for_time_period(self, x1, y1, speed1, angle1, x2, y2, speed2, angle2, seconds=60):
        if x1 == x2 and y1 == y2:
            return "red"

        contr_angles_vertical = angle1 in ("top", "bottom") and angle2 in ("top", "bottom") and angle1 != angle2
        same_x = x1 == x2
        if contr_angles_vertical and same_x:
            if (y1 > y2 and angle1 == "top") or (y2 > y1 and angle2 == "top"):
                pass
            else:
                return "red"

        contr_angles_horizontal = angle1 in ("left", "right") and angle2 in ("left", "right") and angle1 != angle2
        same_y = y1 == y2
        if contr_angles_horizontal and same_y:
            if (x1 > x2 and angle1 == "right") or (x2 > x1 and angle2 == "right"):
                pass
            else:
                return "red"

        semi_contr_angles_vertical = angle1 in ("top", "bottom") and angle2 in ("top", "bottom") and angle1 != angle2
        near_x = abs(x1 - x2) == 1
        if semi_contr_angles_vertical and near_x:
            if (y1 > y2 and angle1 == "top") or (y2 > y1 and angle2 == "top"):
                pass
            else:
                return "yellow"

        semi_contr_angles_horizontal = angle1 in ("left", "right") and angle2 in ("left", "right") and angle1 != angle2
        near_y = abs(y1 - y2) == 1
        if semi_contr_angles_horizontal and near_y:
            if (x1 > x2 and angle1 == "right") or (x2 > x1 and angle2 == "right"):
                pass
            else:
                return "yellow"

        zone_priority = {"red": 1, "yellow": 2, "green": 3}
        zone = "green"
        for sec in range(seconds):
            new_x1, new_y1 = self.get_trajectory_function(x1, y1, speed1, angle1, sec)
            new_x2, new_y2 = self.get_trajectory_function(x2, y2, speed2, angle2, sec)

            new_zone = self.get_zone(new_x1, new_y1, new_x2, new_y2)
            if zone_priority[new_zone] > zone_priority[zone]:
                zone = new_zone

        return zone

    def get_ships_coordinates_and_zones(self):
        ships = self.ship_repo.get_all()
        ship_ids = [s.ship_id for s in ships]

        last_coordinates = {}
        for ship_id in ship_ids:
            last_coord = self.ship_coordinates_repo.get_ship_last_coordinates(ship_id)
            last_coordinates[ship_id] = last_coord

        zones = {}
        zone_priority = {"red": 3, "yellow": 2, "green": 1}
        for ship_id1, coord1 in last_coordinates.items():
            for ship_id2, coord2 in last_coordinates.items():
                if ship_id1 == ship_id2:
                    continue

                zone = self.get_zone_for_time_period(coord1.x, coord1.y, coord1.speed, coord1.vector,
                                                     coord2.x, coord2.y, coord2.speed, coord2.vector)
                curr_zone = zones.get(ship_id1)

                if (not curr_zone) or (zone_priority[zone] > zone_priority[curr_zone]):
                    zones[ship_id1] = zone

            if not zones.get(ship_id1):
                zones[ship_id1] = "green"

        return last_coordinates, zones

    def get_ships_info(self):
        coordinates, zones = self.get_ships_coordinates_and_zones()

        ship_list = []
        for ship_id, coord in coordinates.items():
            ship_list.append({
                "id": ship_id,
                "last_time": coord.time,
                "last_status": zones.get(ship_id),
                "last_speed": coord.speed,
                "last_position": {
                    "x": coord.x,
                    "y": coord.y
                }
            })

        return {"ships": ship_list}

    def get_ship_history(self, ship_id: int):
        ship_coords = self.ship_coordinates_repo.get_all_by_ship_id(ship_id)
        ship_coords = sorted(ship_coords, key=lambda s: s.id, reverse=True)

        status_list = []
        for coord in ship_coords:
            status_list.append({
                "time": coord.time,
                "speed": coord.speed,
                "position": {
                    "x": coord.x,
                    "y": coord.y
                }
            })

        return {"id": ship_id, "positions": status_list}
