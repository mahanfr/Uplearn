from django import forms
from django.contrib.auth import (
    get_user_model,
    password_validation,
    authenticate,
)
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email, ValidationError
from .validator import validate_username

User = get_user_model()

class UserRegisterForm(forms.ModelForm):

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
        "email_in_use": _("Email is already in use"),
    }

    class Meta:
        model = User
        fields = ['user_name', 'email', 'first_name', 'last_name']
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "example@email.com"})
    )

    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=_("Enter the same password as before, for verification."),
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch"
            )
        return password2
    
    def clean_user_name(self):
        user_name = self.cleaned_data["user_name"]
        validate_username(user_name)
        if User.objects.filter(user_name=user_name).count() > 0:
            raise forms.ValidationError(self.error_messages["user_name_in_use"], code="user_name_in_use")
        return user_name

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        validate_email(email)
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(
                self.error_messages["email_in_use"],
                code= "email_in_use"
            )
        return email

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user