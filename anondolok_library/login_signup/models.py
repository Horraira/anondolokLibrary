from django.db import models


class Contact(models.Model):
    c_name = models.CharField(max_length=45, null=True)
    c_mail = models.EmailField(max_length=254, null=True)
    c_phone = models.CharField(max_length=12, null=True)
    c_message = models.TextField(max_length=500, null=True)
