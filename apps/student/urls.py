from django.urls import path
from . import views

urlpatterns = [
  # Class
  path('list', views.StudentListView.as_view() , name='student-list'),
  path('create/', views.AddStudent, name='student-create'),
  path('detail/<int:pk>', views.StudentDetailView.as_view(), name='student-detail'),
  path('update/<int:pk>', views.EditStudent, name='student-update'),
  path('delete/<int:pk>', views.StudentDeleteView.as_view(), name='student-delete'),
]