from django import forms
from .models import Rental


class RentalModelForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = '__all__'

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
        required=False,
        widget=forms.TextInput(     
            attrs={'type': 'date'} 
        )
    )  
    
