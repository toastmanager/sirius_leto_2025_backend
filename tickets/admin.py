from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import Ticket, TicketCategory, TicketType, TicketGroup
from .forms import TicketForm


@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    form = TicketForm
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
    }


class TicketInline(TabularInline):
    form = TicketForm
    model = Ticket
    extra = 0


@admin.register(TicketGroup)
class TicketGroupAdmin(ModelAdmin):
    inlines = [
        TicketInline,
    ]


class TicketTypeInline(TabularInline):
    model = TicketType
    extra = 0


@admin.register(TicketCategory)
class TicketCategoryAdmin(ModelAdmin):
    inlines = [TicketTypeInline]


@admin.register(TicketType)
class TicketTypeAdmin(ModelAdmin):
    pass
