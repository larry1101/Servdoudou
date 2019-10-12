from django.db import models


# Create your models here.

class Chengyu(models.Model):
    word = models.CharField(max_length=20)
    meaning = models.CharField(max_length=256)
    pos = models.IntegerField(default=130)

    def __unicode__(self):
        return self.word
