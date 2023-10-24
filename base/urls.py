from django.urls import path
from . import views


urlpatterns = [
      path("login", views.loginPage, name="login"),
      path("logout", views.logoutUser, name="logout"),
      path("register", views.registerUser, name="register"),
      path("", views.home, name="home"),
      path('room/<str:id>/', views.room, name="room"),
      path('create-room/', views.createRoom, name="create-room"),
      path('update-room/<str:id>', views.updateRoom, name="update-room"),
      path('delete-room/<str:id>', views.deleteRoom, name="delete-room"),
      path('delete-message/<str:id>', views.deleteMessage, name="delete-message"),
      path('my-profile', views.myProfile, name="my-profile"),
      path('user-profile/<str:pk>', views.userProfile, name="user-profile")
]