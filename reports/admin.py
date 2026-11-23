from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):

    list_display = (
        'community',
        'user',
        'status',
        'reason',
        'outage',
        'reported_at',
        'is_verified',
    )

    list_filter = (
        'status',
        'reason',
        'is_verified',
        'reported_at',
    )

    search_fields = (
        'community__name',
        'user__username',
        'description',
    )

    readonly_fields = ('created_at',)

    date_hierarchy = 'reported_at'
