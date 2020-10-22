from django.contrib import admin
from .models import Comment,Video,Like,Favourite,History,Tag,Flag,playlist_video,Playlist
# Register your models here.

admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Favourite)
admin.site.register(History)
admin.site.register(Tag)
admin.site.register(Flag)
admin.site.register(Playlist)
admin.site.register(playlist_video)