from django import forms
from django.contrib.auth.models import User

class ManagerEditForm(forms.ModelForm):
    birthdate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    years_of_experience = forms.IntegerField()
    city = forms.CharField(max_length=100)
    language = forms.CharField(max_length=100, required=False)
    education = forms.CharField(max_length=100, required=False)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False)

    class Meta:
        model = User
        fields = ['username', 'birthdate', 'years_of_experience', 'city', 'language', 'education', 'gender', 'description']

    def __init__(self, *args, **kwargs):
        super(ManagerEditForm, self).__init__(*args, **kwargs)
        # Add any necessary customization or widget settings here if needed
