from django import forms
from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        """Set required and widgets for fields."""
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                }
            )

