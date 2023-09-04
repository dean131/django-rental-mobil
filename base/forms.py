from django import forms
from .models import Rental


class RentalModelForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.TextInput(     
            attrs={'type': 'date'} 
        )
    )  
    end_date = forms.DateField(
        widget=forms.TextInput(     
            attrs={'type': 'date'} 
        )
    )  
    check_out_date = forms.DateField(
        widget=forms.TextInput(     
            attrs={'type': 'date'} 
        )
    )  
    class Meta:
        model = Rental
        fields = '__all__'
