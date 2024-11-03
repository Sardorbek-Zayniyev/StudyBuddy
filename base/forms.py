from django.forms import ModelForm
from .models import Topic, Room, Message


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
