from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MovieRank(models.Model):
    date = models.DateTimeField()
    is_recommended = models.BooleanField()
    review = models.CharField(max_length=1024)
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, default='')

    class Meta:
        verbose_name = 'обзор',
        verbose_name_plural = 'обзоры'
