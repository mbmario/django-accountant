from django import forms
from django.forms import extras
from django import forms

from .models import Category, LineItem

CATEGORIES_LIST = Category.objects.all().values_list('name',flat=True)[::1]
CATEGORIES_TUPLE = zip(CATEGORIES_LIST, CATEGORIES_LIST)

class CatForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    total = forms.DecimalField(label='Total', max_digits=10, decimal_places=2)

class LIForm(forms.Form):

    name = forms.CharField(label='Name', max_length=100)
    category = forms.ChoiceField(choices = CATEGORIES_TUPLE, required=True)
    price = forms.DecimalField(label='Price', max_digits=10, decimal_places=2)
    date = forms.DateField(widget=forms.SelectDateWidget())
    info = forms.CharField(label='Info', max_length=200)

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
