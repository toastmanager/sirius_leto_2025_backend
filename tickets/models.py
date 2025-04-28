from django.db import models
from django.contrib.gis.db import models as gis_models

from users.models import User


class TicketCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    # TODO: add ticket category priority score [from 1 to 10]

    class Meta:
        verbose_name = "Категория заявки"
        verbose_name_plural = "Категории заявок"

    def __str__(self):
        return self.title


class TicketType(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    category = models.ForeignKey(
        TicketCategory, on_delete=models.CASCADE, related_name="types"
    )
    # TODO: add ticket type priority score [from 1 to 10]

    class Meta:
        verbose_name = "Тип заявки"
        verbose_name_plural = "Типы заявок"

    def __str__(self):
        return self.title


class TicketGroup(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    last_created_on = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания последней заявки"
    )
    # TODO: add ticket group status

    class Meta:
        verbose_name = "Группа заявок"
        verbose_name_plural = "Группы заявок"

    @property
    def priority(self) -> int:
        # TODO: Complete this function to take into account the priority scores of types and categories.
        days_diff = (self.last_created_on - self.created_on).days
        ticket_count = self.tickets.count()  # type: ignore
        calculated_priority = (1 + days_diff) * ticket_count
        return calculated_priority

    priority.fget.short_description = "Приоритет"  # type: ignore

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

    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    type = models.ForeignKey(
        TicketType, on_delete=models.CASCADE, related_name="tickets", verbose_name="Тип"
    )
    location = gis_models.PointField(
        srid=4326,
        null=False,
        help_text="Geographic location (longitude, latitude)",
        verbose_name="Координаты",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(
        TicketGroup,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="Группа",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING_REVIEW,
        verbose_name="Статус",
    )
    address = models.CharField(max_length=255, verbose_name="Адрес")

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
