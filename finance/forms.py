from django import forms

from finance.models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "account",
            "category",
            "kind",
            "bucket",
            "amount",
            "date",
            "description"
        ]
        widgets = {
            "date" : forms.DateInput(attrs={"type": "date"})
        }
