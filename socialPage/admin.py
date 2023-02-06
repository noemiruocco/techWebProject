from django.contrib import admin
from .models import UserProfile, Post, Comment, SingleItem, GroceryList

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(SingleItem)
admin.site.register(GroceryList)

