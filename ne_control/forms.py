from django import forms

class ActionTakenForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full border border-gray-300 rounded px-3 py-2'
        })
    )
    previ_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full border border-gray-300 rounded px-3 py-2',
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full h-20 border border-gray-300 rounded px-3 py-2'
        })
    )




