from django import forms

class QAForm(forms.Form):
    question = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Ask your question..."}),
        label="Your Question"
    )
