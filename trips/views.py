from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Trip, LogDay
from .serializers import TripSerializer, LogDaySerializer
from .services import geocode_location, get_route
from .hos_engine import calculate_hos
from .eld_engine import generate_eld_logs

class TripListCreateView(generics.ListCreateAPIView):
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Trip.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        current_location = self.request.data.get("current_location")
        pickup_location = self.request.data.get("pickup_location")
        dropoff_location = self.request.data.get("dropoff_location")
        if not current_location or not pickup_location or not dropoff_location:
            raise ValidationError("All locations are required.")

        current_coords = geocode_location(current_location)
        pickup_coords = geocode_location(pickup_location)
        dropoff_coords = geocode_location(dropoff_location)
        if not current_coords or not pickup_coords or not dropoff_coords:
            raise ValidationError("Location not found.")

        route_data = get_route([current_coords, pickup_coords, dropoff_coords])
        if not route_data:
            raise ValidationError("Route not found.")

        hos_data = calculate_hos(route_data["distance_miles"], route_data["duration_hours"])
        serializer.save(
            owner=self.request.user,
            total_distance=route_data["distance_miles"],
            total_miles=route_data["distance_miles"],
            total_duration=route_data["duration_hours"],
            polyline=route_data["polyline"],
            hos_total_work_hours=hos_data["total_work_hours"],
            hos_driving_days=hos_data["driving_days"],
            hos_cycle_violation=hos_data["cycle_violation"],
            hos_logs=hos_data["logs"]
        )


class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Trip.objects.filter(owner=self.request.user)


class GenerateELDLogsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, trip_id):
        try:
            trip = Trip.objects.get(id=trip_id, owner=request.user)
        except Trip.DoesNotExist:
            return Response({"error": "Trip not found"}, status=404)

        logs = generate_eld_logs(trip)
        trip.log_days.all().delete()
        for log in logs:
            LogDay.objects.create(
                trip=trip,
                date=log["date"],
                segments=log["segments"],
                total_driving=log["total_driving"],
                total_on_duty=log["total_on_duty"],
                total_off_duty=log["total_off_duty"]
            )
        return Response(logs, status=201)


class LogDayListView(generics.ListAPIView):
    serializer_class = LogDaySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        trip_id = self.kwargs.get("trip_id")
        return LogDay.objects.filter(trip__id=trip_id, trip__owner=self.request.user)

class LogDayListView(generics.ListAPIView):
    serializer_class = LogDaySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        trip_id = self.kwargs.get("trip_id")
        user = self.request.user
        
        # 1. On cherche les logs existants
        queryset = LogDay.objects.filter(trip__id=trip_id, trip__owner=user)
        
        # 2. SI VIDE : On force la génération immédiate
        if not queryset.exists():
            try:
                trip = Trip.objects.get(id=trip_id, owner=user)
                logs_data = generate_eld_logs(trip)
                for ld in logs_data:
                    LogDay.objects.create(
                        trip=trip,
                        date=ld["date"],
                        segments=ld["segments"],
                        total_driving=ld.get("total_driving", 0),
                        total_on_duty=ld.get("total_on_duty", 0),
                        total_off_duty=ld.get("total_off_duty", 0)
                    )
                # On rafraîchit le queryset après création
                queryset = LogDay.objects.filter(trip__id=trip_id, trip__owner=user)
            except Trip.DoesNotExist:
                return LogDay.objects.none()

        return queryset.order_by('date')