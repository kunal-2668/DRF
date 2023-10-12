from django.db import models

# Create your models here.



class Stream(models.Model):
    stream = models.CharField(max_length=200)

    def __str__(self):
        return self.stream



class Person(models.Model):
    name= models.CharField(max_length=222)
    age = models.PositiveIntegerField()
    stream = models.ForeignKey(Stream,on_delete=models.SET_NULL,blank=True,null=True,related_name='Streams')

    def __str__(self):
        return self.name