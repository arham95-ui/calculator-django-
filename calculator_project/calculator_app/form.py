from django import forms

class CalculatorForm(forms.Form):
    expression = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter expression (e.g., 2+3*4)',
            'id': 'expression-input'
        })
    )
    
    # No __init__ method needed - Django handles it automatically