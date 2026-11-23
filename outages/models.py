from django.db import models

# Create your models here.
from django.db import models


class Outage(models.Model):

    class Status(models.TextChoices):
        ONGOING = 'ONGOING', 'Ongoing'
        RESTORED = 'RESTORED', 'Restored'

    community = models.ForeignKey(
        'areas.Community',
        on_delete=models.PROTECT,
        related_name='outages'
    )

    started_at = models.DateTimeField()

    restored_at = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ONGOING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.community.name} - {self.get_status_display()}"
