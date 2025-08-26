from django.db import models

# Create your models here.


class WorldBankData(models.Model):

    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=15)
    series = models.CharField(max_length=100)
    year = models.IntegerField()
    value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.country} - {self.series} - {self.year}"

    class Meta:
        unique_together = ('country_code', 'series', 'year')
