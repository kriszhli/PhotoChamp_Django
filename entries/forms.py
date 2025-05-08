from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Entry, EntryReview

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['challenge', 'image', 'title', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Entry'))

class EntryReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 11)],
        widget=forms.RadioSelect
    )

    class Meta:
        model = EntryReview
        fields = ['rating', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Review'))
