from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.question_list_all),
    path('login/', views.login),
    path('signup/', views.signup),
    path('ask/', views.question_add),
    path('popular/', views.question_list_popular),
    path('new/', views.test),
    re_path('question/(?P<id>\d+)/', views.question_page)
]
