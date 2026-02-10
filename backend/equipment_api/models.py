from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Dataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    filename = models.CharField(max_length=255)
    upload_date = models.DateTimeField(default=timezone.now)
    file_size = models.IntegerField(null=True, blank=True)
    row_count = models.IntegerField(null=True, blank=True)
    file_hash = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-upload_date']
        indexes = [
            models.Index(fields=['user', 'upload_date']),
            models.Index(fields=['file_hash']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.filename} - {self.upload_date}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            user_datasets = Dataset.objects.filter(user=self.user, is_active=True)
            if user_datasets.count() >= 5:
                oldest = user_datasets.order_by('upload_date').first()
                oldest.is_active = False
                oldest.save()
        super().save(*args, **kwargs)

class EquipmentData(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment')
    equipment_name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=50)
    flowrate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pressure = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    temperature = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        indexes = [
            models.Index(fields=['dataset', 'equipment_type']),
        ]
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"

class DatasetSummary(models.Model):
    dataset = models.OneToOneField(Dataset, on_delete=models.CASCADE, related_name='summary')
    total_count = models.IntegerField()
    avg_flowrate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    avg_pressure = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    avg_temperature = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_flowrate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_flowrate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_pressure = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_pressure = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_temperature = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_temperature = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Summary for {self.dataset.filename}"

class EquipmentTypeStats(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='type_stats')
    equipment_type = models.CharField(max_length=50)
    count = models.IntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    avg_flowrate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    avg_pressure = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    avg_temperature = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        unique_together = [['dataset', 'equipment_type']]
    
    def __str__(self):
        return f"{self.equipment_type}: {self.count} ({self.percentage}%)"