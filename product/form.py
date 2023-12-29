
from django import forms
from product.models import Comment
from django.forms import ModelForm



#comment-form.............................................................
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form_input input_name', 'placeholder': 'Subject'}),
            'comment': forms.TextInput(attrs={'class': 'form_input input_email', 'placeholder': 'Your comment'}),
            'rate': forms.NumberInput(attrs={'class': 'input_rating', 'placeholder': 'Your Rating', 'min': '1', 'max': '5'}),
        }
#comment-form.............................................................        

