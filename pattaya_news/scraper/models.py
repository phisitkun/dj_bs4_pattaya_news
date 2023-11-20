from django.db import models
from datetime import date, datetime
from phonenumber_field.modelfields import PhoneNumberField
from cloudinary.models import CloudinaryField
from cloudinary import CloudinaryImage

class PageContent(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=150)
    content = models.TextField()
    entry_date = models.DateTimeField(default=datetime.now)
    json=models.JSONField()

    def __str__(self):
        return self.url
    

    
