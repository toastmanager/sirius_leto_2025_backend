from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth import get_user_model

User = get_user_model()


class TicketCategory(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Категория заявки"
        verbose_name_plural = "Категории заявок"

    def __str__(self):
        return self.title


class TicketType(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        TicketCategory, on_delete=models.CASCADE, related_name="types"
    )

    class Meta:
        verbose_name = "Тип заявки"
        verbose_name_plural = "Типы заявок"

    def __str__(self):
        return self.title


class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.ForeignKey(
        TicketType, on_delete=models.CASCADE, related_name="tickets"
    )
    location = gis_models.PointField(
        srid=4326, null=False, help_text="Geographic location (longitude, latitude)"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return self.title

    @property
    def latitude(self):
        return self.location.y

    @property
    def longitude(self):
        return self.location.x
