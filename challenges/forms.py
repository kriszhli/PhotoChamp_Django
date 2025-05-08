from django import forms
from django.forms import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import Challenge

# Model Form Advantage: Builds form fields that match model’s fields, no need to declare each field
class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'slug', 'description', 'start_date', 'end_date', 'tags']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date':   DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['start_date'].widget.attrs.update({'placeholder': 'YYYY-MM-DD'})
        self.fields['end_date'].widget.attrs.update({'placeholder': 'YYYY-MM-DD'})

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('title', placeholder='Challenge Name'),
            Field('slug', placeholder='URL Slug (unique)'),
            Field('description', placeholder='Brief description…', rows=3),
            Field('start_date'),
            Field('end_date'),
            Field('tags', placeholder='Comma-separated tags'),
            Submit('save', 'Save Challenge', css_class='btn btn-primary')
        )
