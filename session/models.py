from django.db import models


class Session(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self):
        return f'{self.start_year} -> {self.end_year}'
