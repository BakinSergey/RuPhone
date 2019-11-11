from django.db import models


# 800;1010000;1019999;10000;ПАО "Ростелеком";Уральский федеральный округ, Приволжский федеральный округ
class PhoneRange(models.Model):
    code = models.IntegerField(db_index=True)
    start = models.IntegerField(db_index=True)
    finish = models.IntegerField()
    provider = models.CharField(max_length=140)
    region = models.CharField(max_length=100)
