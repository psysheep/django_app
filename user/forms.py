from django import forms
from django.contrib.auth.forms import UserCreationForm  # default django user creation form
from django.contrib.auth.models import User  # built-in django user model


class RegistrationForm(UserCreationForm):  # overriding or extending the UserCreationForm
    email = forms.EmailField(required=True)  # add email as UserCreationForm does not have this field by default
    country = forms.CharField(required=True, max_length=20)

    class Meta:
        model = User  # Creating a User model
        fields = ['username', 'email', 'country', 'password1', 'password2']
        # Specifying the fields that we want to have

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
