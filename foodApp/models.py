from django.db import models


class Subscriber(models.Model):
    title = models.CharField(max_length=10)
    description = models.TextField()