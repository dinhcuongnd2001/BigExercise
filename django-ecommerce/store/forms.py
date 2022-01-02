from django import forms
from django.forms import fields,FileInput
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import RATING, Review, Customer

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30,widget=forms.TextInput(attrs={'class': 'text-field username'}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class': 'text-field email'}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'text-field'}))
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput(attrs={'class': 'text-field'}))

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError("Error password!")
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Error account!")
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("Account already exists!")

    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'],email=self.cleaned_data['email'],password=self.cleaned_data['password1'])

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment','rate']

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'first-name-field'}),
            'last_name': forms.TextInput(attrs={'class': 'last-name-field'}),
            'email': forms.EmailInput(attrs={'class': 'email-field'}),
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone','image']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'phone-field'}),
            'image': FileInput(),
        }
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'image-field'})
        self.fields['image'].label='Change avatar '
        self.fields['image'].currently=''
    