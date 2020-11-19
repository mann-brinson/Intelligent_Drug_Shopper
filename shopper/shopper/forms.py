from django import forms

class TreatmentForm(forms.Form):
	condition = forms.CharField(max_length=100, required=True)
	price_high = forms.IntegerField(required=True)
	current_med = forms.CharField(max_length=100, required=False)
