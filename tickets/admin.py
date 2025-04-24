from django.contrib import admin

from .models import Ticket, TicketCategory, TicketType, TicketGroup
from .forms import TicketForm


class TicketAdmin(admin.ModelAdmin):
    form = TicketForm


class TicketInline(admin.TabularInline):
    form = TicketForm
    model = Ticket
    extra = 0


class TicketGroupAdmin(admin.ModelAdmin):
    inlines = [
        TicketInline,
    ]


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketGroup, TicketGroupAdmin)
admin.site.register(TicketCategory)
admin.site.register(TicketType)
