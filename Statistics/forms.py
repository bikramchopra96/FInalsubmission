from django import forms
from .models import YearlyTable


# creating a form
class AddForm(forms.ModelForm):
    
    class Meta:
        # specify model to be used
        model = YearlyTable

        # specify fields to be used
        fields = [
            "timestamp",
            "high",
            "low",
            "open",
            "close",
            "volume"
        ]
