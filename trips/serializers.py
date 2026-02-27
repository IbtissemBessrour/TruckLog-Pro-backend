from rest_framework import serializers
from .models import Trip, LogDay

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"
        read_only_fields = (
            "owner",
            "total_distance",
            "total_duration",
            "total_miles",
            "polyline",
            "hos_total_work_hours",
            "hos_driving_days",
            "hos_cycle_violation",
            "hos_logs",
            "created_at"
        )

class LogDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogDay
        fields = "__all__"
        read_only_fields = ("trip",)