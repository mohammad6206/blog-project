from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

class Category(models.Model):  
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    image = models.ImageField(upload_to='blog/', default='blog/default.jpg')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ManyToManyField(Category)  
    counted_view = models.IntegerField(default=0)  
    status = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_date']


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status:
            self.published_date = timezone.now()
        else:
            self.published_date = None
        super().save(*args, **kwargs)



class ContactMessage(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField()
    subject = models.CharField(max_length=255, blank=True, null=True)
    message=models.CharField(max_length=255)
    created_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.name
    
class ContactReply(models.Model):
    message = models.ForeignKey('ContactMessage', on_delete=models.CASCADE, related_name='replies')
    reply_text = models.TextField()
    replied_at = models.DateTimeField(auto_now_add=True)
    replied_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Reply to: {self.message.name}"



class pakages(models.Model):
    image = models.ImageField(upload_to='blog/', default='blog/default.jpg')
    name=models.CharField(max_length=255)
    description=models.TextField()
    status = models.BooleanField(default=False)
    hotel=models.CharField(max_length=255)
    hotel_stars = models.CharField(
        max_length=5,
        choices=[('★', '⭐'), ('★★', '⭐⭐'), ('★★★', '⭐⭐⭐'), ('★★★★', '⭐⭐⭐⭐'), ('★★★★★', '⭐⭐⭐⭐⭐')],
        default='★★★'
    )
    max_count = models.IntegerField(validators=[MinValueValidator(1)])
    price=models.IntegerField()
    Number_of_nights=models.IntegerField()
    location=models.CharField(max_length=255)

    def __str__(self):
        return self.name
    



class CustomUser(AbstractUser):
    
    login_count = models.IntegerField(default=0)
    ip=models.GenericIPAddressField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username