from rest_framework import permissions, generics

from .serializers import TicketSerializer
from .permissions import OwnTicketPermission
from .models import Ticket


class TicketListView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all().order_by("-created_at")
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the tickets
        for the currently authenticated user.
        """

        user = self.request.user
        if user and user.is_authenticated:
            return Ticket.objects.filter(user=user).order_by("-created_at")
        return Ticket.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        OwnTicketPermission,
    ]
    queryset = Ticket.objects.all()
