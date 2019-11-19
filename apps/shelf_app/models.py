from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self,data):
        errors={}
        if len(data['email'])<=0:
            errors['email']='Input Email'
        if len(data['password'])<=0:
            errors['password']='Input Password'
        if len(data['password'])>=10:
            errors['password']='Password must be under 10 characters'
        EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data['email']):
            errors['email']='Invalid email-address'
        if len(User.objects.filter(email=data['email']))!=0:
            errors['email']='email is already in use'
        if data['password'] != data['comfirm_password']:
            errors['password']='passwords do not match'
        return errors

class User(models.Model):
    email=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class StoreManager(models.Manager):
    def basic_validator(self,data):
        errors={}
        if len(data['store_name'])<=0:
            errors['name']='Input Store Name'
        return errors

class Store(models.Model):
    name=models.CharField(max_length=50)
    users=models.ManyToManyField(User, related_name='stores')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=StoreManager()

class Location(models.Model):
    address=models.CharField(max_length=120)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    zip_code=models.IntegerField()
    store=models.ForeignKey(Store, related_name='locations')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Aisle(models.Model):
    description=models.CharField(max_length=50)
    location=models.ForeignKey(Location, related_name='aisles')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Item(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    location=models.ForeignKey(Location, related_name='items')
    aisle=models.ForeignKey(Aisle, related_name='items')
    users=models.ManyToManyField(User,related_name='items')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

