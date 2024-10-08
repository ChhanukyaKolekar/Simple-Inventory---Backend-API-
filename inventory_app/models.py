from django.db import models

# Create your models here.

class Items(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField()
    price=models.FloatField()

    def __str_(self):
        return self.name