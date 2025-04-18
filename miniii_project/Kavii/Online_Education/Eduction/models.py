from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True,null=True,upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    profile_image = models.ImageField(blank=True,null=True,upload_to='teacher_images/')
    total_likes = models.IntegerField(default=0)
    profile_url = models.URLField(blank=True,null=True,default="#")
    
    def total_courses(self):
        return self.courses.count()
    def total_videos(self):
        return sum(course.videos.count() for course in self.courses.all())
    
    def total_likes(self):
        return sum(video.likes for course in self.courses.all() for video in course.videos.all())
    def total_views(self):
        return sum(video.views for course in self.courses.all() for video in course.videos.all())

    def __str__(self):
        return self.name


class Course(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.title


class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.title


class ContactRequest(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    number = models.CharField(max_length=15)
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
