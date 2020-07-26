from django.urls import path,include
from . import views

urlpatterns = [
    path('login', views.Login_view.as_view(),name="login"),
    path('home', views.Home_view.as_view(),name="home"),
    path('logout', views.LogoutView.as_view(),name="logout"),
    path('view/<int:id>', views.PostsView.as_view(),name="view_record"),
    path('tag/<int:id>', views.AddtagView.as_view(),name="add_tag"),
    path('delete/<int:id>', views.delete,name="delete"),
    
]