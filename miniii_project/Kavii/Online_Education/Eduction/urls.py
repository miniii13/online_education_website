from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('', HomePageView.as_view(), name='home'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('update/', update_profile, name='update_profile'),
    path('logout/', User_logout, name='logout'),
    path('courses/', CoursesView.as_view(), name='course'),
    path('teachers/', TeachersView.as_view(), name='Teacher'),
    path('about-us/', AboutUsView.as_view(), name='about'),
    path('contact-us', ContactView.as_view(), name='contact'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('teacher-profile/<int:pk>/', TeacherProfileView.as_view(), name='teacher_profile'),
    path('course/<int:pk>/', CoursePlaylistView.as_view(), name='course_playlist'),
    path("contact-us/", contact_us, name="contact_us"),
    path('courses/search/', course_search, name='course_search'),
    
    
        

]
