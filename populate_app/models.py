from django.db import models
from django.conf import settings



class Question(models.Model):
  
    name = models.CharField(max_length=50, null=False, blank=False)
    type = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    answer = models.CharField(max_length=50, null=False, blank=False)
    count = models.IntegerField()
    percentage = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False, default=0.0
    )
    
    
    
    
    
