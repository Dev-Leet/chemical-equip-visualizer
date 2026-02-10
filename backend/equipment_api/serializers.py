from rest_framework import serializers
from .models import Dataset, EquipmentData, DatasetSummary, EquipmentTypeStats

class EquipmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentData
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']

class DatasetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'upload_date', 'row_count', 'file_size', 'is_active']

class DatasetDetailSerializer(serializers.ModelSerializer):
    equipment = EquipmentDataSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'upload_date', 'row_count', 'file_size', 'is_active', 'equipment']

class DatasetSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetSummary
        fields = '__all__'

class EquipmentTypeStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentTypeStats
        fields = '__all__'

class SummaryResponseSerializer(serializers.Serializer):
    dataset_id = serializers.IntegerField()
    filename = serializers.CharField()
    upload_date = serializers.DateTimeField()
    statistics = serializers.DictField()
    type_distribution = serializers.ListField()