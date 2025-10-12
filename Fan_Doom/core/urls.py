# En tu archivo core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('follow_author/', views.follow_author, name='follow_author'),
    path('follow_work/', views.follow_work, name='follow_work'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('author_work_register/', views.author_work_register, name='author_work_register'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('fandom/<int:fandom_id>/', views.fandom_detail, name='fandom_detail'),
    path('vote/', views.vote, name='vote'),
    path('wiki/<int:page_id>/', views.wiki_page_detail, name='wiki_page_detail'),
]
