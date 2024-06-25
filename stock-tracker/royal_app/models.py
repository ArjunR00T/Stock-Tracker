from django.db import models
from django import forms

    	

# Create your models here.
class product(models.Model):
	name=models.CharField(max_length=50)
	cp=models.DecimalField(decimal_places=2,max_digits=10)
	sp=models.DecimalField(decimal_places=2,max_digits=10)
	nos=models.IntegerField()

	def __str__(self):
		return self.name

class purchases(models.Model):
	name =models.CharField(max_length=50)
	cost=models.DecimalField(decimal_places=2,max_digits=10)
	date=models.DateTimeField()
	nos=models.IntegerField()
	payment=models.BooleanField()

class recordForm(forms.Form):
	name = forms.CharField(max_length=100);
	cp = forms.DecimalField(max_digits=5);
	sp = forms.DecimalField(max_digits=5);
	qty = forms.IntegerField(max_value=999);
