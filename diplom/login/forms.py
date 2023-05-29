from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Income, Account, Spending


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or ' \
                                            'fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too ' \
                                             'similar to your other personal information.</ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as ' \
                                             'before, for verification.</small></span>'


class IncomeAddingForm(ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'time', 'category', 'paymentMethod']

    def __init__(self, *args, **kwargs):
        super(IncomeAddingForm, self).__init__(*args, **kwargs)
        self.fields['amount'].label = 'Кількість'
        self.fields['time'].label = 'Час'
        self.fields['category'].label = 'Категорія'
        self.fields['paymentMethod'].label = 'Метод'


class SpendingAddingForm(ModelForm):
    class Meta:
        model = Spending
        fields = ['amount', 'time', 'category', 'paymentMethod']

    def __init__(self, *args, **kwargs):
        super(SpendingAddingForm, self).__init__(*args, **kwargs)
        self.fields['amount'].label = 'Кількість'
        self.fields['time'].label = 'Час'
        self.fields['category'].label = 'Категорія'
        self.fields['paymentMethod'].label = 'Метод'


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def default_settings(self, firstName, lastName, email):
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].label = 'First Name'
        self.fields['first_name'].initial = firstName

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].label = 'Last Name'
        self.fields['last_name'].initial = lastName

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].label = 'Email'
        self.fields['email'].initial = email

class ProfileImageForm(ModelForm):
    class Meta:
        model = Account
        fields = ['image']
