from django.contrib import admin
from .models import Dataset, EquipmentData, DatasetSummary, EquipmentTypeStats

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'upload_date', 'row_count', 'is_active']
    list_filter = ['is_active', 'upload_date']
    search_fields = ['filename', 'user__username']

@admin.register(EquipmentData)
class EquipmentDataAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'dataset']
    list_filter = ['equipment_type']
    search_fields = ['equipment_name', 'equipment_type']

@admin.register(DatasetSummary)
class DatasetSummaryAdmin(admin.ModelAdmin):
    list_display = ['dataset', 'total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature']

@admin.register(EquipmentTypeStats)
class EquipmentTypeStatsAdmin(admin.ModelAdmin):
    list_display = ['dataset', 'equipment_type', 'count', 'percentage']
    list_filter = ['equipment_type']