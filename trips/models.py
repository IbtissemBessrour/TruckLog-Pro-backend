from django.db import models
from django.conf import settings

class Trip(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_trips'
    )
    current_location = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)

    total_distance = models.FloatField(null=True, blank=True)
    total_duration = models.FloatField(null=True, blank=True)
    total_miles = models.FloatField(null=True, blank=True)
    polyline = models.JSONField(null=True, blank=True)

    hos_total_work_hours = models.FloatField(null=True, blank=True)
    hos_driving_days = models.IntegerField(null=True, blank=True)
    hos_cycle_violation = models.BooleanField(default=False)
    hos_logs = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trip {self.id} - {self.owner.email}"


class LogDay(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='log_days')
    date = models.DateField()
    segments = models.JSONField()  # [{"start":0,"end":6,"status":"OFF"},...]
    total_driving = models.FloatField(default=0)
    total_on_duty = models.FloatField(default=0)
    total_off_duty = models.FloatField(default=0)

    def __str__(self):
        return f"LogDay {self.date} - Trip {self.trip.id}"