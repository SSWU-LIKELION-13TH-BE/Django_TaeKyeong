from django.urls import path
from .views import signup_view, login_view, password_search, mypage_view, update_user_view, my_posts_view, delete_my_post, edit_post_view
from django.contrib.auth import views as auth_views

app_name= 'user'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/',login_view,name='login'),
    path('password_search/',password_search,name='password_search'),
    path('password_email/', auth_views.PasswordResetView.as_view(template_name='user/registration/password_reset_form.html'),name='password_email'), 
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('mypage/', mypage_view, name='mypage'),
    path('mypage/update/', update_user_view, name='update_user'),
    path('mypage/my_posts', my_posts_view, name='my_posts'),
    path('mypage/my_posts/<int:pk>/delete/', delete_my_post, name='delete_my_post'),
    path('mypage/my_posts/<int:pk>/edit/', edit_post_view, name='edit_post'),

]