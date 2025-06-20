from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator



class Category(models.Model):  
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Post(models.Model):
    image = models.ImageField(upload_to='blog/', default='blog/default.jpg')
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ManyToManyField(Category)  
    counted_view = models.IntegerField(default=0)  
    status = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_date']


    def __str__(self):
        return self.title



class ContactMessage(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField()
    subject = models.CharField(max_length=255, blank=True, null=True)
    message=models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class pakages(models.Model):
    image = models.ImageField(upload_to='blog/', default='blog/default.jpg')
    name=models.CharField(max_length=255)
    description=models.TextField()
    status = models.BooleanField(default=False)
    hotel=models.CharField(max_length=255)
    hotel_stars = models.CharField(
        max_length=5,
        choices=[('★', '1 Star'), ('★★', '2 Stars'), ('★★★', '3 Stars'), ('★★★★', '4 Stars'), ('★★★★★', '5 Stars')],
        default='★★★'
    )
    max_count = models.IntegerField(validators=[MinValueValidator(1)])
    price=models.IntegerField()
    Number_of_nights=models.IntegerField()
    location=models.CharField(max_length=255)

    def __str__(self):
        return self.name