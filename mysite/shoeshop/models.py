from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class User(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	phone =  models.CharField(max_length=120)
	address = models.CharField(max_length=120)

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField(default=0)
	size = models.FloatField()
	colour = models.CharField(max_length=200)

class CartItem(models.Model):
	cart = models.ForeignKey('Cart', null=True, blank=True)
	product = models.ForeignKey(Product)
	quantity = models.IntegerField(default=1)

class Cart(models.Model):
	total = models.DecimalField(max_digits=100, decimal_places=2,

class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
	order_id = models.CharField(max_length=120, default='ABC', unique=True)
	cart = models.ForeignKey(Cart)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#instance.profile.save()

