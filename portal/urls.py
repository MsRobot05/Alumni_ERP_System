# portal/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # (Your existing dashboard URL)
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('announcements/', views.announcements, name='announcements'),
    
    # --- !! THESE ARE THE MISSING LINES !! ---
    path('hiring/', views.hiring_posts_view, name='hiring'),
    path('meetups/', views.meetup_posts_view, name='meetups'),
    path('alumni/', views.alumni_list_view, name='alumni_list'),
    path('post/new/', views.create_post_view, name='create_post'),
]