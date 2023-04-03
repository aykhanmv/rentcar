from django.urls import path,re_path
from user.views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', AccountRegistrationView.as_view(), name='register'),
    path('logout/', logout, name='logout'),
    path('profile/', MyCarsView.as_view(), name='profile'),
    path('profile/edit/', ProfileSettingsView, name='profile_edit'),
    path("forget/", ForgetPasswordView.as_view(), name="forget"),
    path("forget/done/",ForgetPasswordDoneView.as_view(), name="forget-done"),
    path(
        "forget/<uidb64>/<token>/",
        ForgetPasswordResetConfirmView.as_view(),
        name="forget-reset-confirm",
    ),
    path("forget/complete/", ForgetPasswordCompleteView.as_view(), name="forget-complete"),

    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,33})/$',
        Activate.as_view(), name='activate'),
]