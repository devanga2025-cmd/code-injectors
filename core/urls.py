from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('book-demo/', views.book_demo_view, name='book_demo'),
    path('signup/', views.auth_view, name='signup'),
    path('login/', views.auth_view, name='login'),
    path('auth/', views.auth_view, name='auth'),
    path('scan/', views.scan_view, name='scan'),
    path('try-free/', views.try_free_view, name='try_free'),
    path('try/', views.try_free_view, name='try_free_alias'),
    path('auth/github/', views.oauth_github, name='oauth_github'),
    path('auth/github/callback/', views.oauth_github_callback, name='oauth_github_callback'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('api/lead/', views.capture_lead, name='capture_lead'),
    path('api/scan/', views.run_scan_api, name='run_scan_api'),
    path('path/to/logo.png', views.serve_logo, name='serve_logo_sample_path'),
    path('assent/logo.png', views.serve_logo, name='serve_logo_assent'),
]

