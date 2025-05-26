from django.urls import path
from .views import dashboard, results, history_detail, user_login, user_signup, user_logout, CustomPasswordResetView, CustomPasswordResetConfirmView
from django.contrib.auth import views as auth_views
from advisor import views

urlpatterns = [
    path('', user_login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('results/', results, name='results'),
    path('history_detail/<int:pk>/', history_detail, name='history_detail'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
]
