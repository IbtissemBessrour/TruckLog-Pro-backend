from django.urls import path
from .views import TripListCreateView, TripDetailView, GenerateELDLogsView, LogDayListView

urlpatterns = [
    path('', TripListCreateView.as_view(), name='trip-list'),
    path('<int:pk>/', TripDetailView.as_view(), name='trip-detail'),
    path('<int:trip_id>/generate_eld/', GenerateELDLogsView.as_view(), name='generate-eld'),
    path('<int:trip_id>/logs/', LogDayListView.as_view(), name='trip-logs'),
]