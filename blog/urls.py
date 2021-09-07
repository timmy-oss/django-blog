from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('posts/<int:id>/comments/', views.add_comment_view, name='comment'),
    path('posts/today/', views.today_post_view, name='today_post'),
    path('posts/most-popular/', views.popular_posts_view, name='popular_posts'),
    path('posts/latest/', views.latest_posts_view, name='latest_posts'),
    path('posts/<slug:slugname>/', views.post_view, name='post'),
    path('posts/<slug:slugname>/vote/<int:vote>/', views.vote_view, name='vote'),
    path('categories/<slug:slugname>/', views.category_view, name='category'),
    path('sign-out/', views.sign_out_view, name='sign_out'),
    path('sign-in/', views.sign_in_view, name='sign_in'),
    path('accounts/login/', views.sign_in_view, name='sign_in'),
    path('sign-up/', views.sign_up_view, name='sign_up'),





]
