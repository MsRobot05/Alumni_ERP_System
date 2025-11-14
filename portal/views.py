# portal/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from accounts.models import AlumniUser
from django.utils import timezone
from .forms import PostForm # <-- Make sure you've created portal/forms.py

@login_required
def dashboard_view(request):
    # This is the dashboard, it only DISPLAYS posts
    all_posts = Post.objects.all()
    upcoming_meetups = Post.objects.filter(
        post_type='Meetup', 
        meetup_time__gte=timezone.now()
    ).order_by('meetup_time')
    
    open_roles = Post.objects.filter(post_type='Hiring')
    
    stats = {
        'total_alumni': AlumniUser.objects.count(),
        'open_roles': open_roles.count(),
        'upcoming_meetups': upcoming_meetups.count(),
    }

    context = {
        'user': request.user,
        'posts': all_posts,
        'stats': stats,
        'upcoming_meetups': upcoming_meetups,
        'jobs_announcements': open_roles,
    }
    return render(request, 'portal/dashboard.html', context)

# --- THIS IS THE VIEW FOR THE "+ NEW POST" BUTTON ---
@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('dashboard')
    else:
        form = PostForm()
        
    context = {
        'form': form
    }
    return render(request, 'portal/create_post.html', context)

# --- THESE ARE YOUR SIDEBAR PAGE VIEWS ---
@login_required
def hiring_posts_view(request):
    # Get all posts that are 'Hiring'
    hiring_posts = Post.objects.filter(post_type='Hiring').order_by('-created_at')
    
    context = {
        'posts': hiring_posts,
    }
    return render(request, 'portal/hiring.html', context)
@login_required
def announcements(request):
    return render(request, 'portal/announcements.html')
@login_required
def meetup_posts_view(request):
    # Get all posts that are 'Meetup'
    meetup_posts = Post.objects.filter(post_type='Meetup').order_by('-created_at')
    
    context = {
        'posts': meetup_posts,
    }
    return render(request, 'portal/meetups.html', context)

@login_required
def alumni_list_view(request):
    # Get all users, ordered by batch year
    all_alumni = AlumniUser.objects.all().order_by('-batch_year', 'full_name')
    
    context = {
        'alumni': all_alumni,
    }
    return render(request, 'portal/alumni_list.html', context)