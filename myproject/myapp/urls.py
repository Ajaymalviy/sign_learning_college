from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_views, name='login'), 
    path('signup/', views.signup_view, name='signup'), 
    path('logout/', views.logout, name='logout'), 
    path('speech-to-text/', views.speech_to_text, name='speech_to_text'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
