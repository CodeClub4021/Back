# myapp/forms.py
from django import forms
from .models import Coach, Rating

"""class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ['name', 'address']"""

class CoachForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
