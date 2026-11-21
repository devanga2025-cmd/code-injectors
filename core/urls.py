from django.urls import path
from . import views

urlpatterns = [
    # Marketing & Public Pages
    path('', views.landing_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('book-demo/', views.book_demo_view, name='book_demo'),
    path('signup/', views.auth_view, name='signup'),
    path('login/', views.auth_view, name='login'),
    path('auth/', views.auth_view, name='auth'),
    path('scan/', views.scan_view, name='scan'),
    path('try-free/', views.try_free_view, name='try_free'),
    path('try/', views.try_free_view, name='try_free_alias'),
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),

    # GitHub OAuth Flow & Compatibility Endpoints
    path('auth/github/', views.oauth_github, name='oauth_github'),
    path('auth/github/callback/', views.oauth_github_callback, name='oauth_github_callback'),
    path('auth/github/callback', views.oauth_github_callback, name='oauth_github_callback_noslash'),
    path('accounts/github/login/callback/', views.oauth_github_callback, name='oauth_github_callback_allauth'),
    path('accounts/github/login/callback', views.oauth_github_callback, name='oauth_github_callback_allauth_noslash'),
    path('accounts/github/login/', views.oauth_github, name='oauth_github_login_compat'),
    path('accounts/github/login', views.oauth_github, name='oauth_github_login_compat_noslash'),
    path('github/callback/', views.oauth_github_callback, name='oauth_github_callback_short'),
    path('github/callback', views.oauth_github_callback, name='oauth_github_callback_short_noslash'),
    path('oauth/github/callback/', views.oauth_github_callback, name='oauth_github_callback_alt'),
    path('oauth/github/callback', views.oauth_github_callback, name='oauth_github_callback_alt_noslash'),
    path('logout/', views.logout_view, name='logout'),

    # Professional Enterprise Dashboard & Sidebar Sub-views
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/reporting/', views.dashboard_view, {'tab': 'reporting'}, name='dashboard_reporting'),
    path('dashboard/projects/', views.dashboard_view, {'tab': 'projects'}, name='dashboard_projects'),
    path('dashboard/code/', views.dashboard_view, {'tab': 'code'}, name='dashboard_code'),
    path('dashboard/secrets/', views.dashboard_view, {'tab': 'secrets'}, name='dashboard_secrets'),
    path('dashboard/supply-chain/', views.dashboard_view, {'tab': 'supply_chain'}, name='dashboard_supply_chain'),
    path('dashboard/scans/', views.dashboard_view, {'tab': 'scans'}, name='dashboard_scans'),
    path('dashboard/settings/', views.dashboard_view, {'tab': 'settings'}, name='dashboard_settings'),

    # Standalone Sub-page Aliases for direct navigation
    path('reporting/', views.dashboard_view, {'tab': 'reporting'}, name='reporting'),
    path('projects/', views.dashboard_view, {'tab': 'projects'}, name='projects'),
    path('code/', views.dashboard_view, {'tab': 'code'}, name='code'),
    path('secrets/', views.dashboard_view, {'tab': 'secrets'}, name='secrets'),
    path('supply-chain/', views.dashboard_view, {'tab': 'supply_chain'}, name='supply_chain'),
    path('scans/', views.dashboard_view, {'tab': 'scans'}, name='scans'),
    path('settings/', views.dashboard_view, {'tab': 'settings'}, name='settings'),

    # Dashboard Actions & Security Scanning APIs
    path('api/github/sync/', views.sync_github_repos_api, name='api_github_sync'),
    path('api/github/disconnect/', views.disconnect_github_api, name='api_github_disconnect'),
    path('api/repos/connect/', views.connect_repo_api, name='api_connect_repo'),
    path('api/repos/<int:repo_id>/scan/', views.trigger_repo_scan_api, name='api_repo_scan'),
    path('api/scans/<str:scan_id>/status/', views.scan_status_api, name='api_scan_status'),
    path('api/banner/dismiss/', views.dismiss_banner_api, name='api_dismiss_banner'),
    path('api/feedback/', views.submit_feedback_api, name='api_submit_feedback'),
    path('api/reporting/data/', views.reporting_data_api, name='api_reporting_data'),
    path('api/reporting/export/', views.reporting_export_api, name='api_reporting_export'),
    path('api/findings/<str:finding_id>/status/', views.update_finding_status_api, name='api_finding_status'),
    path('api/findings/<str:finding_id>/details/', views.finding_details_api, name='api_finding_details'),
    path('api/lead/', views.capture_lead, name='capture_lead'),
    path('api/scan/', views.run_scan_api, name='run_scan_api'),

    # Asset Fallbacks
    path('path/to/logo.png', views.serve_logo, name='serve_logo_sample_path'),
    path('assent/logo.png', views.serve_logo, name='serve_logo_assent'),
]
