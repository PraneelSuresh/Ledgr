from django import forms

from finance.models import Transaction, Category, User

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

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Amount must be positive.")
        return amount


class CategoryForm(forms.ModelForm):
    model = Category
    fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        user = User.objects.get(username="demo")
        qs = Category.objects.filter(name=name, user=user)
        if self.instance.pk:
            qs.exclude(pk=self.instance)
        if qs.exists():
            raise forms.ValidationError(f"You already have a category named {name}")
        return name
