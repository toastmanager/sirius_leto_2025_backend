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


class TicketGroup(models.Model):
    title = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    last_created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Группа заявок"
        verbose_name_plural = "Группы заявок"

    def __str__(self):
        return self.title


class Ticket(models.Model):
    STATUS_PENDING_REVIEW = "PENDING_REVIEW"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_REJECTED = "REJECTED"

    STATUS_CHOICES = (
        (STATUS_PENDING_REVIEW, "Принята на рассмотрение"),
        (STATUS_IN_PROGRESS, "Работы ведутся"),
        (STATUS_COMPLETED, "Работы завершены"),
        (STATUS_REJECTED, "Отказано"),
    )

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
    group = models.ForeignKey(
        TicketGroup, on_delete=models.CASCADE, related_name="tickets"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING_REVIEW,
        verbose_name="Статус",
    )

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
