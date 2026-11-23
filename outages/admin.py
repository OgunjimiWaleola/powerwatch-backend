from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Outage


@admin.register(Outage)
class OutageAdmin(admin.ModelAdmin):

    list_display = (
        'community',
        'status',
        'started_at',
        'restored_at',
        'created_at',
    )

    list_filter = (
        'status',
        'community',
        'started_at',
    )

    search_fields = (
        'community__name',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    date_hierarchy = 'started_at'
