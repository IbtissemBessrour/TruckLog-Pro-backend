import math

def calculate_hos(total_miles, total_duration):
    """
    Calcule les HOS (Hours of Service) d'un trip
    en intégrant les règles :
    - max 11h driving/day
    - 70h / 8 days cycle
    - 1h pickup, 1h dropoff
    - fuel stop every 1000 miles (30 min ON DUTY)
    """
    max_drive_per_day = 11  # heures
    driving_days = math.ceil(total_duration / max_drive_per_day)

    # Fuel stops
    fuel_stops = math.floor(total_miles / 1000)
    fuel_stop_hours = fuel_stops * 0.5  # 30 min = 0.5 h ON DUTY

    # Total work hours = driving + pickup/dropoff + fuel stops
    total_work_hours = total_duration + 2 + fuel_stop_hours

    cycle_limit = 70  # 70h / 8 days
    cycle_violation = total_work_hours > cycle_limit

    logs = {
        "daily_limit": max_drive_per_day,
        "cycle_limit": cycle_limit,
        "estimated_driving_days": driving_days,
        "fuel_stops": fuel_stops,
        "fuel_stop_hours": fuel_stop_hours,
        "total_work_hours": total_work_hours
    }

    return {
        "total_work_hours": total_work_hours,
        "driving_days": driving_days,
        "cycle_violation": cycle_violation,
        "logs": logs
    }