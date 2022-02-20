from django.contrib.auth import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db import models
# Create your models here.


# Create your models here.
class Services_Type(models.Model):
    services_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class Services_Level(models.Model):
    services_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class Paper_type(models.Model):
    paper_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='0')
    order_price=models.CharField(max_length=255)
    media_file=models.FileField(upload_to='media/order_media')
    topic=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    deadline=models.DateField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.topic)
