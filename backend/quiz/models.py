from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capital = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "countries"
    
    def __str__(self):
        return f"{self.name} - {self.capital}"