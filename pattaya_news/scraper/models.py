from django.db import models
from datetime import date, datetime
from phonenumber_field.modelfields import PhoneNumberField
from cloudinary.models import CloudinaryField
from cloudinary import CloudinaryImage

class PageContent(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True, null=True)
    img_url = models.URLField(blank=True, null=True)
    entry_date = models.DateTimeField(default=datetime.now)
    json=models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.url
    

    
