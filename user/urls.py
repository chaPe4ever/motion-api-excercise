from django.urls import path

from user.views import ListCreateUserView, RetrieveUpdateDestroyUserView

urlpatterns = [
    path("", ListCreateUserView.as_view(), name="user-list-create"),
    path("<int:pk>/", RetrieveUpdateDestroyUserView.as_view(), name="user-detail"),
]
