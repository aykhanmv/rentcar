
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import forms as f
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.template import loader
from django.utils.translation import gettext_lazy as _


# get custom user
User = get_user_model()



class MyUserLoginForm(AuthenticationForm):
    error_messages = {
        # **AuthenticationForm.error_messages,
        "login_mismatch": _(
            "The password or email is incorrect. Please make sure you type it correctly."
        ),
        **AuthenticationForm.error_messages,
        # 'is_blocked': _("This account is blocked."),
    }

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            user = User.objects.filter(email=email).first()
            if user and not user.is_active:
                raise forms.ValidationError(
                    self.error_messages["inactive"],
                    code="inactive",
                )

            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages["login_mismatch"],
                    code="login_mismatch",
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def clean_username(self):
        # print(self.cleaned_data,'clean_username')
        email = self.cleaned_data.get("username")
        user = User.objects.filter(email__iexact=email).first()
        if user:
            return user.email
        return email.lower()


class BaseRegistrationForm(forms.ModelForm):

    error_messages = {
        "password_incorrect": _("Incorrect password"),
        "password_mismatch": _("The two password fields didn't match."),

        "phone_unique": _(
            "This phone number is already registered. Please enter a different phone number."
        ),
        "phone_invalid": _(
            "This phone number is invalid. Please enter a valid phone number."
        ),
        "short_password": _(
            "This password is too short. It must contain at least 8 characters."
        ),
        "not_proper_passowd": _(
            "Password must contain at least one UPPERCASE letter and and one NUMBER."
        ),
        "gov_id_unique": _(
            "The gov id is already registered by another account."
        ),
        "gov_id_invalid": _(
            "Invalid gov id."
        ),
        "only_english_letters": _(
            "Only english letters are allowed."
        ),
    }

    password = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        label=_("Repeat password"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."),
    )

    full_name = forms.CharField(
        label=_("Name and Surname"),
        max_length=255,
        error_messages={
            "required": _("Please enter your name and surname"),
            "max_length": _(
                "Your name and surname must be less than 255 characters"
            ),
        },
    )

    class Meta:
        model = User
        fields = (
            "full_name",
            "email",
            "gov_id",
            "user_choices",
            "voen_code",
            "phone",
            "gender",
            "social_media",
        )
        labels = {
            "full_name": "Name, Surname",
            "voen_code": "Voen code",
            "gov_id": "Passport number",
            "phone": "Telefon",
            "user_choices": "User type",
            "email": "Email",
            "gender": "Cins",
            "social_media": "Sosial media",
        }
        widgets = {
            "email": forms.EmailInput(attrs={}),   
        }
        help_texts = {
            'gov_id': _("After prefix 7 symbols are needed. For example: AA1234567 or AZE1234567")
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = (
            "user_choices",
            "full_name",
            # "gov_id",
            # "voen_code",
            "email",
            # "accept_rules",
            # "phone",

        )
        for field in required_fields:
            if field in self.fields and not self.fields[field].required:
                self.fields[field].required = True

        self.fields["user_choices"].empty_label = None
        self.fields["gender"].empty_label = None
    def clean_full_name(self):

        if not len(self.cleaned_data["full_name"].split()) == 2:
            raise forms.ValidationError(
                _(
                    "Enter the correct first and last name separated by spaces"
                )
            )

        return self.cleaned_data["full_name"]
    def clean_email(self):
        form_email = self.cleaned_data.get("email")
        return form_email.lower()

    def clean_password(self):
        password = self.cleaned_data.get("password")
        
        has_uppercase = False
        has_number = False

        for char in password:
            if char.isdigit() and not has_number:
                has_number = True
            if char.isupper() and not has_uppercase:
                has_uppercase = True

            if has_number and has_uppercase:
                break

        if len(password) < 8:
            raise forms.ValidationError(self.error_messages["short_password"])
        elif not has_uppercase or not has_number:
            raise forms.ValidationError(self.error_messages["not_proper_passowd"])
        else:
            return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password_confirm

    def save(self, commit=True):
        user = super(BaseRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])

        first_name, last_name = self.cleaned_data["full_name"].split()
        user.first_name = first_name
        user.last_name = last_name

        if commit:
            user.save()
        return user
    
class AccountUpdateModelForm(forms.ModelForm):
    error_messages = {
        "phone_unique": _(
            "A user with this phone number is already exists!"
        ),
        "phone_invalid": _(
            "Enter the las 7 digits only (without prefix)"
        ),
    }
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            format="%d/%m/%Y",
            attrs={
                "type": "date",
            },
        ),
        label=_("Birth date"),
    )
    class Meta:
        model = User
        fields = (
            "profile_picture",
            "first_name",
            "last_name",
            "address",
            "phone",
            # "gender",
            "date_of_birth",
        )
        labels = {
            "first_name": _("Name"),
            "last_name": _("Surname"),
            "address": _("Company address"),
            "phone": _("Phone number"),
            "date_of_birth": _("Birth date"),

        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].required = False

class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }), max_length=255)