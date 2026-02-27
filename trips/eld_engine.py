from datetime import datetime, timedelta

def generate_eld_logs(trip):
    logs = []
    total_hours = trip.hos_total_work_hours or trip.total_duration
    remaining_hours = total_hours
    current_date = datetime.utcnow().date()

    # Fuel stops à distribuer comme ON DUTY (0.5h chacun)
    fuel_stop_hours = trip.hos_logs.get("fuel_stop_hours", 0)

    while remaining_hours > 0:
        day_hours = min(11, remaining_hours)
        off_hours = max(0, 24 - day_hours - 1)  # 1h pickup/dropoff
        segments = [
            {"start": 0, "end": off_hours, "status": "OFF"},
            {"start": off_hours, "end": off_hours + 1 + fuel_stop_hours, "status": "ON"},  # ON inclut fuel stops
            {"start": off_hours + 1 + fuel_stop_hours, "end": off_hours + 1 + fuel_stop_hours + day_hours, "status": "DRIVING"}
        ]
        logs.append({
            "date": current_date.isoformat(),
            "segments": segments,
            "total_driving": day_hours,
            "total_on_duty": day_hours + 1 + fuel_stop_hours,
            "total_off_duty": off_hours
        })
        remaining_hours -= day_hours
        current_date += timedelta(days=1)

    return logs