from django.contrib import admin

from .models import User, Topic, Room, Message

admin.site.register(User)

admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Message)
