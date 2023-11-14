from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from cloudinary.models import CloudinaryField
from cloudinary import CloudinaryImage

class PageContent(models.Model):
    url = models.URLField()
    content = models.TextField()
    json=models.JSONField()

    def __str__(self):
        return self.url
    

    
