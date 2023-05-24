from django.urls import path
from .views import home, signup, signin, sign_out, activate

app_name = "authentication"
urlpatterns = [
    path("", home, name="home"),
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
    path("signout/", sign_out, name="sign_out"),
    path("activate/<str:uidb64>/<str:token>/", activate, name="activate"),
]





