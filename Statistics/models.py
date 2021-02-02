from django.db import models

# Create your models here.
class YearlyTable(models.Model):
    productdate = models.DateTimeField(auto_now_add=True,auto_now=False)
    index = models.IntegerField()
    timestamp = models.DateTimeField()
    high = models.DecimalField(decimal_places=2, max_digits=7)
    low = models.DecimalField(decimal_places=2, max_digits=7)
    open = models.DecimalField(decimal_places=2, max_digits=7)
    close = models.DecimalField(decimal_places=2, max_digits=7)
    volume = models.BigIntegerField()