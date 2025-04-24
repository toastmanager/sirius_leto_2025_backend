from django.urls import path

from .views import TicketDetailView, TicketListView

app_name = "tickets"

urlpatterns = [
    path("", TicketListView.as_view(), name="list"),
    path("<int:pk>/", TicketDetailView.as_view(), name="detail"),
]
