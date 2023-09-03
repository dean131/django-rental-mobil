from django import forms
from .models import Rental


class RentalModelForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = '__all__'