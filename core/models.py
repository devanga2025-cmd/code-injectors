import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DemoRequest(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    github_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    github_username = models.CharField(max_length=150, blank=True, null=True)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)
    github_access_token = models.CharField(max_length=255, blank=True, null=True)
    provider = models.CharField(max_length=50, default='GitHub')
    banner_dismissed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.provider})"

class Repository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repositories')
    name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=300)
    owner = models.CharField(max_length=150)
    is_private = models.BooleanField(default=False)
    default_branch = models.CharField(max_length=100, default='main')
    html_url = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    # Status & Scan Tracking
    scan_status = models.CharField(
        max_length=50, 
        choices=[
            ('not_scanned', 'Not Scanned'),
            ('queued', 'Queued'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='not_scanned'
    )
    last_scan_date = models.DateTimeField(blank=True, null=True)
    code_findings_count = models.IntegerField(default=0)
    supply_chain_findings_count = models.IntegerField(default=0)
    secrets_findings_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        unique_together = ('user', 'full_name')

    def __str__(self):
        return f"{self.full_name} ({self.scan_status})"

class SecurityScan(models.Model):
    scan_id = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='scans')
    status = models.CharField(
        max_length=50,
        choices=[
            ('not_scanned', 'Not Scanned'),
            ('queued', 'Queued'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='queued'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # Vulnerability counts
    critical_count = models.IntegerField(default=0)
    high_count = models.IntegerField(default=0)
    medium_count = models.IntegerField(default=0)
    low_count = models.IntegerField(default=0)
    secrets_count = models.IntegerField(default=0)
    supply_chain_count = models.IntegerField(default=0)
    
    duration_ms = models.FloatField(default=1.4)
    log_output = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.scan_id} - {self.repository.name} ({self.status})"

class SecurityFinding(models.Model):
    finding_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    scan = models.ForeignKey(SecurityScan, on_delete=models.CASCADE, related_name='findings')
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='findings')
    rule_id = models.CharField(max_length=150)
    category = models.CharField(
        max_length=50,
        choices=[
            ('code', 'Code Vulnerability'),
            ('secrets', 'Exposed Secret'),
            ('supply_chain', 'Supply Chain'),
        ],
        default='code'
    )
    severity = models.CharField(
        max_length=20,
        choices=[
            ('CRITICAL', 'Critical'),
            ('HIGH', 'High'),
            ('MEDIUM', 'Medium'),
            ('LOW', 'Low'),
            ('INFO', 'Informational'),
        ],
        default='MEDIUM'
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ('open', 'Open'),
            ('in_progress', 'In Progress'),
            ('fixed', 'Fixed'),
            ('ignored', 'Ignored'),
            ('accepted_risk', 'Accepted Risk'),
        ],
        default='open'
    )
    reachability = models.CharField(
        max_length=30,
        choices=[
            ('reachable', 'Reachable'),
            ('unreachable', 'Unreachable'),
            ('unknown', 'Unknown'),
        ],
        default='unknown'
    )
    file_path = models.CharField(max_length=300)
    line_number = models.IntegerField(default=1)
    message = models.TextField()
    remediation = models.TextField()
    code_snippet = models.TextField(blank=True, default='')
    
    first_detected_at = models.DateTimeField(default=timezone.now)
    last_detected_at = models.DateTimeField(default=timezone.now)
    fixed_at = models.DateTimeField(blank=True, null=True)
    ignored_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.severity}] {self.rule_id} in {self.file_path}"

    def save(self, *args, **kwargs):
        if not self.finding_id:
            self.finding_id = f"CS-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

class FeedbackSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    feedback_type = models.CharField(max_length=50, default='scanner')
    scanner_component = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback from {self.user.username if self.user else 'Anonymous'} ({self.created_at.strftime('%Y-%m-%d')})"
