from django import forms
from django.contrib.auth.models import User

class ManagerEditForm(forms.ModelForm):
    birthdate = forms.DateField()
    years_of_experience = forms.IntegerField()
    city = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'birthdate', 'years_of_experience', 'city']
