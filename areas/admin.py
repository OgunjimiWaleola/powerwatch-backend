from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    DistributionCompany,
    Feeder,
    Transformer,
    Community,
)


@admin.register(DistributionCompany)
class DistributionCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'is_active', 'created_at')
    search_fields = ('name', 'short_name')
    list_filter = ('is_active',)


@admin.register(Feeder)
class FeederAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'distribution_company',
        'voltage_level',
        'is_active',
    )
    search_fields = ('name', 'code', 'distribution_company__name')
    list_filter = ('is_active', 'distribution_company')


@admin.register(Transformer)
class TransformerAdmin(admin.ModelAdmin):
    list_display = ('name', 'feeder', 'capacity_kva', 'is_active')
    search_fields = ('name', 'code', 'feeder__name')
    list_filter = ('is_active',)


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'city',
        'state',
        'local_government',
        'transformer',
        'is_active',
    )
    search_fields = (
        'name',
        'street_address',
        'city',
        'local_government',
    )
    list_filter = ('state', 'city', 'is_active')
