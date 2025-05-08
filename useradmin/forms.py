import re
from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit
from .models import UserProfile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = None

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', placeholder='Username'),
            Field('password'),
            Submit('signUp', 'Sign Up', css_class='btn btn-primary w-100 mt-3'),
        )

    def clean_password(self):
        pw = self.cleaned_data.get('password')
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,16}$'
        if not re.match(pattern, pw):
            raise forms.ValidationError(
                "Password must be 8–16 characters, include 1 uppercase, 1 lowercase & 1 number."
            )
        return pw

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model  = UserProfile
        fields = [
            'bio',
            'profile_pic',
            'website',         # <— added
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('bio', placeholder='Tell us about yourself…'),
            Field('profile_pic'),
            Field('website', placeholder='Your website (https://…)'),
            Submit('save', 'Save Profile', css_class='btn btn-primary w-100 mt-3'),
        )