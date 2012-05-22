from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from reviews.models import ReviewedItem


class ReviewedItemForm(ModelForm):
    """
    The ReviewedItem add/edit form.
    """
    SCORE_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    score = forms.ChoiceField(label=_('Rating'), required=True, 
        choices=SCORE_CHOICES, widget=forms.Select(attrs={'class': 'star'}), 
        error_messages={
            'required': _("Please choose a rating for this item."),
            'invalid_choice': _("Please choose a rating for this item.")
        })
    content = forms.CharField(label=_('Review'), required=True, help_text='', 
        widget=forms.Textarea, error_messages={
            'required': _("Please write what you think of this item.")
        })
    
    class Meta:
        model = ReviewedItem
        fields = (
            'score',
            'content',
        )
