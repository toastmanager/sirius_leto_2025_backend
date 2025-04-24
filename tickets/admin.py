from django.contrib import admin

from .models import Ticket, TicketCategory, TicketType
from .forms import TicketForm


class TicketAdmin(admin.ModelAdmin):
    form = TicketForm


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketCategory)
admin.site.register(TicketType)
