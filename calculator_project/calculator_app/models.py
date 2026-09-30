# calculator_app/models.py
from django.db import models
from django.contrib.auth.models import User

class CalculationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    expression = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.expression} = {self.result}"