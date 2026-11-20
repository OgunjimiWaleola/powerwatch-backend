from django.db import models

# Create your models here.

from django.db import models


class DistributionCompany(models.Model):
    name = models.CharField(max_length=150, unique=True)
    short_name = models.CharField(max_length=30, unique=True)
    headquarters = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_name


class Feeder(models.Model):
    distribution_company = models.ForeignKey(
        DistributionCompany,
        on_delete=models.PROTECT,
        related_name='feeders'
    )

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, blank=True)
    voltage_level = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['distribution_company', 'name'],
                name='unique_feeder_name_per_disco'
            )
        ]

    def __str__(self):
        return f"{self.distribution_company.short_name} - {self.name}"


class Transformer(models.Model):
    feeder = models.ForeignKey(
        Feeder,
        on_delete=models.PROTECT,
        related_name='transformers',
        null=True,
        blank=True
    )

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, blank=True)
    capacity_kva = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Community(models.Model):
    name = models.CharField(max_length=150)
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='Lagos')
    local_government = models.CharField(max_length=100, blank=True)

    transformer = models.ForeignKey(
        Transformer,
        on_delete=models.SET_NULL,
        related_name='communities',
        null=True,
        blank=True
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'street_address', 'city', 'state'],
                name='unique_community_location'
            )
        ]

    def __str__(self):
        return f"{self.name}, {self.city}"
