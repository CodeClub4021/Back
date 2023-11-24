# myapp/forms.py
from django import forms
from .models import Gym, Rating

class GymForm(forms.ModelForm):
    class Meta:
        model = Gym
        fields = ['name', 'address']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
