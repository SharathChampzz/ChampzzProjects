from django import forms

class TextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Enter Text') # name attribute will have this variable value
