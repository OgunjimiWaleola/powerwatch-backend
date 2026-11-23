from django.conf import settings
from django.db import models


class Report(models.Model):

    class Status(models.TextChoices):
        POWER_OFF = 'OFF', 'Power Off'
        POWER_BACK = 'ON', 'Power Back'

    class Reason(models.TextChoices):
        GRID_FAULT = 'GRID_FAULT', 'Grid Fault'
        LOAD_SHEDDING = 'LOAD_SHEDDING', 'Scheduled Load Shedding'
        LOCAL_FAULT = 'LOCAL_FAULT', 'Local Fault'
        UNKNOWN = 'UNKNOWN', 'Not Sure'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='reports'
    )

    community = models.ForeignKey(
        'areas.Community',
        on_delete=models.PROTECT,
        related_name='reports'
    )

    outage = models.ForeignKey(
        'outages.Outage',
        on_delete=models.SET_NULL,
        related_name='reports',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=3,
        choices=Status.choices
    )

    reason = models.CharField(
        max_length=20,
        choices=Reason.choices,
        default=Reason.UNKNOWN
    )

    description = models.TextField(blank=True)

    reported_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['-reported_at']
        indexes = [
            models.Index(fields=['community', '-reported_at']),
            models.Index(fields=['status', '-reported_at']),
        ]

    def __str__(self):
        return f"{self.community.name} - {self.get_status_display()}"
