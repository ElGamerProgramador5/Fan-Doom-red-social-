
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home, name='home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('author/register-work/', views.author_work_register, name='author_work_register'),
    path('logout/', views.logout_view, name='logout'),
    path('follow_author/', views.follow_author, name='follow_author'),
    path('follow_work/', views.follow_work, name='follow_work'),
]