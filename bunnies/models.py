from django.conf import settings
from django.db import models

from rest_framework.exceptions import ValidationError

# Create your models here.


class RabbitHole(models.Model):
    '''
    Rabbits live in rabbit holes
    '''
    location = models.CharField(max_length=64, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bunnies_limit = models.PositiveIntegerField(default=5)


class Bunny(models.Model):
    '''

    '''
    name = models.CharField(max_length=64)
    home = models.ForeignKey(RabbitHole, on_delete=models.CASCADE, related_name='bunnies')

    def save(self, *args, **kwargs):
        # Can't save the bunny if the home we try to put it in, has reached
        # its bunny limit
        home = self.home
        if home.bunnies.count() >= home.bunnies_limit:
            raise ValidationError("Hole filled")
        return super().save(*args, **kwargs)
