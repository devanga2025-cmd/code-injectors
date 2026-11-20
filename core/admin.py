from django.contrib import admin
from .models import DemoRequest, UserProfile, Repository, SecurityScan, SecurityFinding, FeedbackSubmission

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

@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'scan_status', 'code_findings_count', 'last_scan_date')
    search_fields = ('name', 'full_name', 'owner')
    list_filter = ('scan_status', 'is_private')

@admin.register(SecurityScan)
class SecurityScanAdmin(admin.ModelAdmin):
    list_display = ('scan_id', 'repository', 'status', 'critical_count', 'high_count', 'started_at')
    search_fields = ('scan_id', 'repository__name')
    list_filter = ('status',)

@admin.register(SecurityFinding)
class SecurityFindingAdmin(admin.ModelAdmin):
    list_display = ('rule_id', 'repository', 'severity', 'category', 'status', 'file_path')
    search_fields = ('rule_id', 'message', 'file_path')
    list_filter = ('severity', 'category', 'status')

@admin.register(FeedbackSubmission)
class FeedbackSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_type', 'rating', 'created_at')
