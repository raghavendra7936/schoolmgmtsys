from django.urls import path
from . import views

urlpatterns = [
  # Class
  path('students', views.StudentListView.as_view() , name='result-studentlist'),
  path('studentresult/<int:stid>', views.ShowTestCycleResults , name='result-viewstudentresult'),
  path('addsubjectresult/<int:stid>', views.CreateTestResult , name='result-addstudentresult'),
  path('edittcresult/<int:pk>', views.EditTCResult , name='result-editstudentresult'),
  path('deletetcresult/<int:pk>', views.DeleteTestResult.as_view(), name='result-deletestudentresult')
]