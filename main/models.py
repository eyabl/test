from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm


class LOVGest(models.Model):
    CodeGestionnaire = models.CharField(max_length=10)
    NomSociete = models.CharField(max_length=50)


class LOVGestForm(ModelForm):
    class Meta:
        model = LOVGest
        fields = ['CodeGestionnaire', 'NomSociete']
        widgets = {
            'CodeGestionnaire': forms.TextInput(attrs={'class': 'form-control'}),
            'NomSociete': forms.TextInput(attrs={'class': 'form-control'})
        }


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class iexps(models.Model):
    numFichier = models.IntegerField()
    etape = models.CharField(max_length=50)
    traitement = models.CharField(max_length=50)
    duree = models.CharField(max_length=50)
