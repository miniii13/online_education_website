from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Teacher
from django.views.generic import DetailView
from .models import Course, ContactRequest, Profile



def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['pass']
        confirm_password = request.POST['c_pass']
        profile_pic = request.FILES['profile_pic']
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('register')

        try:
            user = User.objects.create_user(username=name, email=email, password=password)
            user.save()

            user.profile.profile_pic = profile_pic
            user.profile.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')

        except ValidationError as e:
            messages.error(request, f"Error: {e}")
            return redirect('register')
    else:
        return render(request, 'register.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'login.html')

def User_logout(request):
    logout(request)
    return redirect('/')


@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        old_password = request.POST.get('old_pass')
        new_password = request.POST.get('new_pass')
        confirm_password = request.POST.get('c_pass')
        name = request.POST.get('name')
        email = request.POST.get('email')
        profile_pic = request.FILES.get('profile_pic')
        if old_password and not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect('update_profile')
        if name:
            user.username = name
        if email:
            user.email = email
        if new_password:
            if new_password == confirm_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)
            else:
                messages.error(request, "New passwords do not match.")
                return redirect('update_profile')
        if profile_pic:
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            user.profile.profile_pic = fs.url(filename)
            user.profile.save()
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'update.html')


class HomePageView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all().select_related('teacher')
        return context


class CoursesView(LoginRequiredMixin, TemplateView):
    template_name = "courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all().select_related('teacher')
        return context


class TeachersView(LoginRequiredMixin, TemplateView):
    template_name = "teachers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search_box', '')
        if query:
            context['teachers'] = Teacher.objects.filter(
                Q(name__icontains=query) |
                Q(courses__title__icontains=query) |
                Q(courses__videos__title__icontains=query)
            ).distinct().prefetch_related('courses__videos')
        else:
            context['teachers'] = Teacher.objects.prefetch_related('courses__videos').all()
        return context


class AboutUsView(LoginRequiredMixin, TemplateView):
    template_name = "about_us.html"

class ContactView(LoginRequiredMixin, TemplateView):
    template_name = "contact.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"




class TeacherProfileView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'teachers_profile.html'
    context_object_name = 'teacher'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        teacher = self.get_object()
        context['total_courses'] = teacher.total_courses()
        
        context['total_videos'] = teacher.total_videos()
        context['views'] = teacher.total_views()
        
        return context


class CoursePlaylistView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'playlist_details.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['videos'] = course.videos.all()
        
        return context

@login_required
def contact_us(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        number = request.POST.get("number")
        message = request.POST.get("msg")
        ContactRequest.objects.create(
            name=name,
            email=email,
            number=number,
            message=message
        )
        messages.success(request, "Your request has been sent to the admin.")
        return redirect('contact_us')

    return render(request, "contact.html")

@login_required
def course_search(request):
    search_query = request.GET.get('search_box', '')
    if search_query:
        courses = Course.objects.filter(title__icontains=search_query)
    else:
        courses = Course.objects.all()
    
    return render(request, 'courses.html', {'courses': courses, 'search_query': search_query})
