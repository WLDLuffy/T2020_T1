from django.contrib import admin
from django.urls import path
import DBSmartplanner.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DBSmartplanner.views.login, name = 'login'),
    path('home/', DBSmartplanner.views.home, name = 'home'),
    
]
