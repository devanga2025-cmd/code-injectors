from django.contrib import admin
from .models import DemoRequest, UserProfile

@admin.register(DemoRequest)
class DemoRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'status')
    search_fields = ('email',)
    list_filter = ('status', 'created_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'github_username', 'provider', 'created_at')
    search_fields = ('user__username', 'github_username', 'user__email')
    list_filter = ('provider', 'created_at')
