from django import forms

from .models import SearchForm_m

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class SearchForm(forms.ModelForm):
	# database = forms.CharField(label='', 
	# 			widget=forms.TextInput(attrs={"placeholder": "Put database here"}))
	database = forms.ChoiceField(choices=[(x, x) for x in ('world', 'kickstarter', 'alumni')])
	searchterm = forms.CharField(label='Search', 
				widget=forms.TextInput(attrs={"placeholder": "Enter search term here"}))
	class Meta:
		model = SearchForm_m
		fields = [
			'database',
			'searchterm'
		]

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)

class TreatmentForm(forms.Form):
	condition = forms.CharField(max_length=100, required=True)
	price_high = forms.IntegerField(required=True)
	current_med = forms.CharField(max_length=100, required=False)
