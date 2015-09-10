import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
    
class Budget(models.Model):
    members = models.ManyToManyField(User)
    name = models.CharField(max_length=30)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name
    
class Accounts(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    bankName = models.CharField(max_length=60,null=True,blank=True)
    comment = models.CharField(max_length=60,null=True,blank=True)
    number=models.IntegerField(null=True,blank=True)
    amount = models.FloatField()
    members=models.ManyToManyField(User)

    
class Contractors(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    budget=models.ForeignKey(Budget,blank=True,null=True)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name
    
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    limit=models.IntegerField(null=True)
    budget=models.ForeignKey(Budget,blank=True,null=True)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name
    
class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    category=models.ForeignKey(Category)
    budget=models.ForeignKey(Budget,blank=True,null=True)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name
    
class Expenses(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    date = models.DateField('date published')
    amount = models.FloatField()
    user=models.ForeignKey(User)
    account=models.ForeignKey(Accounts)
    contractor=models.ForeignKey(Contractors,null=True,blank=True)
    subcategory=models.ForeignKey(Subcategory)
    fixed=models.BooleanField(blank=True)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name
    def was_published_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Income(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    date = models.DateField('date published')
    amount = models.FloatField()
    user=models.ForeignKey(User)
    account=models.ForeignKey(Accounts)
    contractor=models.ForeignKey(Contractors,null=True,blank=True)
    fixed=models.BooleanField(blank=True)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name
    

    