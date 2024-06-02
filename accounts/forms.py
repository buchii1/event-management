from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm)
from django.utils.translation import gettext_lazy as _

# Custome user model
userModel = get_user_model()

class NewUserForm(UserCreationForm):
    """
    New User Registration Form
    """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = userModel
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        # Remove autofocus attribute from the username field
        self.fields['username'].widget.attrs.pop('autofocus', None)
    
    def clean(self):
        """
        Additional form validation
        Checks if the username already exist in the database
            and adds an error message if it does

        Returns:
        - cleaned_data (dict): Dictionary containing cleaned form data
        """
        cleaned_data = super(NewUserForm, self).clean()
        username = cleaned_data.get('username')
        if username and userModel.objects.filter(username__iexact=username).exists():
            self.add_error("username", "A user with this username already exist")
        return cleaned_data


class UserLoginForm(AuthenticationForm):
    """
    User Login Form
    """
    error_messages = {
        'invalid_login': _("Please enter a valid username and password."),
    }

    class Meta:
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        # Clear the username field if there are errors
        if self.errors:
            self.data = self.data.copy()
            self.data['username'] = ''