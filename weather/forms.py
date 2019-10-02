from django.forms import ModelForm, TextInput
from django import forms

from .models import City

class CityForm(ModelForm):

    name = forms.CharField()

    class Meta:
        model = City
        fields = ['name']
        # widgets = {'name' : TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'})}


    def clean(self, *args, **kwargs):
        city = self.cleaned_data.get('city')

        name_qs = City.objects.filter(name=city)
        if name_qs.exists():
            raise forms.ValidationError("{} has already been entered".format(name))
