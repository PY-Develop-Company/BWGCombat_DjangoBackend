from django.core.management.base import BaseCommand
from django.core import serializers
from app_name.models import ModelName1, ModelName2  # Import your models

class Command(BaseCommand):
    help = 'Export data to JSON file'

    def handle(self, *args, **kwargs):
        data = serializers.serialize('json', ModelName1.objects.all())
        with open('modelname1_data.json', 'w') as f:
            f.write(data)
        
        data = serializers.serialize('json', ModelName2.objects.all())
        with open('modelname2_data.json', 'w') as f:
            f.write(data)
        
        self.stdout.write(self.style.SUCCESS('Data export completed successfully'))