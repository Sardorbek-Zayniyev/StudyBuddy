from django import forms
from .models import User, Room, Message
from .validators import allow_only_images_validator


class UserForm(forms.ModelForm):

    avatar = forms.FileField(
        widget=forms.FileInput(), validators=[allow_only_images_validator]
    )

    class Meta:
        model = User
        fields = [
            "avatar",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "bio",
        ]


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ["host", "participants"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["body"]
