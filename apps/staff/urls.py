from django.urls import path
from . import views

urlpatterns = [
  # Staff
  path('list', views.StaffListView.as_view() , name='staff-list'),
  path('create/', views.AddStaff, name='staff-create'),
  path('detail/<int:pk>', views.StaffDetailView.as_view(), name='staff-detail'),
  path('update/<int:pk>', views.EditStaff, name='staff-update'),
  path('delete/<int:pk>', views.StaffDeleteView.as_view(), name='staff-delete'),
]