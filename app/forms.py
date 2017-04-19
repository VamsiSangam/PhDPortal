"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import *

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class SynopsisForm(ModelForm):
    class Meta:
        model = Thesis
        fields = ['synopsis']

class ThesisForm(ModelForm):
    class Meta:
        model = Thesis
        fields = ['thesis']

#class sampleForm(ModelForm):
   
#    designation = forms.CharField(max_length = 30, help_text="Please enter the category name.")
#    phone_number = models.CharField(max_length = 16, help_text="Please enter the URL of the page.")
#    class Meta:
#        model = sample
#        fields = ('designation','phone_number')

class RefereeForm(ModelForm):
    class Meta:
        model = Referee
        exclude = ['user', 'added_by']

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(RefereeForm, self).__init__(*args, **kwargs)
        self.fields['type'].required = True
        self.fields['university'].required = False
        self.fields['designation'].required = True
        self.fields['website'].required = False
        

class UserForm(ModelForm):
    first_name = models.CharField(help_text="FirstName: ")
    last_name = models.CharField(help_text="LastName: ")
    email = models.CharField(help_text="Email: ")
    username = models.CharField(help_text="Usename: ")
    is_active = models.BooleanField(forms.HiddenInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['first_name'].required = True
        self.fields['last_name'].required = False
        self.fields['email'].required = True
        self.fields['username'].required = True