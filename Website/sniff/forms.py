from django import forms

class AddressForm(forms.Form):
    mac_address = forms.CharField(label='Mac Address ', max_length=100)
	
	
	
class ShiftsForm(forms.Form):
    mac_address = forms.CharField(label='Mac Address ', max_length=100)