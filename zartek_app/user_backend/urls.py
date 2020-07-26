from django.urls import path,include
from . import views

urlpatterns = [
    path('posts', views.main_class.as_view()),
    path('posts/<id>', views.post_detail.as_view()),
    path('posts/reactions/<id>', views.Reactionlist.as_view()),
]