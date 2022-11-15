from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Post)
admin.site.register(Notification)
admin.site.register(FollowUser)
