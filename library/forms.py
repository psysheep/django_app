from django import forms
from user.models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])

    class Meta:
        model = Review
        fields = ('rating', 'subject', 'text')
