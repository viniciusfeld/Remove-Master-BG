from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=128, null=False)
    email = models.CharField(max_length=64, null=False)
    message = models.CharField(max_length=512, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name