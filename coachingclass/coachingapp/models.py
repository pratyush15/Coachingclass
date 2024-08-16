import datetime 
from datetime import date 
from django.db import models
from django.contrib.auth.models import User  
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
#Create model category 
class Category(models.Model): 
    title=models.CharField(max_length=100) 
    desc=models.TextField()

#Create model image 
class Image(models.Model): 
    title=models.CharField(max_length=100)     
    image=models.ImageField(upload_to="media") 
    added_date=models.DateTimeField() 
    cat=models.ForeignKey(Category,on_delete=models.CASCADE)  

    def __str__(self): 
        return self.title      
    
class Customer(models.Model): 
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    name=models.CharField(max_length=40)  
    mobile=models.IntegerField(
        validators=[
            MinValueValidator(0000000000), 
            MaxValueValidator(9999999999)
        ]
    )
    email=models.EmailField(max_length=50)    
    bday = models.DateField(null=True, blank=True)

    def __str__(self): 
        return self.name  

    def days_until_birthday(self):
        today = date.today() 
        birthday = self.bday.replace(year=today.year)
        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)
        return (birthday - today).days
 