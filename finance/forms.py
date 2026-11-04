from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from finance.models import Transaction, Category, User, Account


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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if "bucket" in self.fields:
            current_choices = list(self.fields["bucket"].choices)

            if current_choices and current_choices[0][0] in ("", None):
                current_choices[0] = ("", "Select a Bucket")
                self.fields["bucket"].choices = current_choices
        if user is not None:
            self.fields["account"].queryset = Account.objects.filter(user=user)
            self.fields["category"].queryset = Category.objects.filter(user=user)
            for field_name, field in self.fields.items():
                if field_name in ['kind', 'category', 'bucket', 'account']:
                    field.widget.attrs.update({'class': 'filter-select'})
                else:
                    field.widget.attrs.update({'class': 'field-input'})

                if not field.widget.attrs.get('placeholder'):
                    field.widget.attrs['placeholder'] = field.label or field_name.capitalize()
        self.fields["category"].empty_label = "Select a Category"
        self.fields["account"].empty_label = "Select an Account"

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Amount must be positive.")
        return amount


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        name = self.cleaned_data["name"]
        qs = Category.objects.filter(name=name, user=self.user)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(f"You already have a category named {name}")
        return name


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["username"].widget.attrs.update({
            "placeholder": "Ada Lovelace    ",
            "autocomplete": "username",
            "autofocus": True,
        })
        self.fields["email"].widget.attrs.update({
            "placeholder": "you@domain.com"
        })
        self.fields["password1"].label = "Password"
        self.fields["password1"].help_text = None
        self.fields["password1"].widget.attrs.update({
            "placeholder": "At least 8 characters",
            "autocomplete": "new-password",
        })
        self.fields["password2"].label = "Confirm password"
        self.fields["password2"].widget.attrs.update({
            "placeholder": "Repeat your password",
            "autocomplete": "new-password",
        })

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["kind", "opening_balance", "name"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if "kind" in self.fields:
            current_choices = list(self.fields["kind"].choices)

            if current_choices and current_choices[0][0] in ("", None):
                current_choices[0] = ("", "Select a Kind")
                self.fields["kind"].choices = current_choices

        for field_name, field in self.fields.items():
            field.widget.use_required_attribute = lambda initial: False

    def clean_name(self):
        name = self.cleaned_data["name"]
        qs = Account.objects.filter(name=name, user=self.user)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(f"You already have an account named {name}")
        return name
