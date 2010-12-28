from django.db import models


class Other(models.Model):
    pass


class EverythingModel(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    username = models.CharField(max_length=20, unique=True)
    address_city = models.CharField(max_length=50)
    address_post_code = models.CharField(max_length=10)
    address = models.TextField()
    o1 = models.ForeignKey(Other)
    something = models.TextField()
    birthday = models.DateTimeField()
    age = models.PositiveSmallIntegerField()
    icon = models.ImageField(upload_to='.')
