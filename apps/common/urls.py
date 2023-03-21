from django.urls import path

from . import homeviews, classviews, acadyeartermviews, classsectionviews, subjectviews, testcycleviews

urlpatterns = [
  # home
  path('', homeviews.IndexView.as_view(), name='home'),

  # Class
  path('class/', classviews.ClassGradeListView.as_view(), name='class-list'),
  path('class/create/', classviews.CreateClassGrade, name='class-create'),
  path('class/update/<int:pk>', classviews.EditClassGrade, name='class-update'),
  path('class/delete/<int:pk>', classviews.DeleteClassGrade.as_view(), name='class-delete'),

  # Academic Year
  path('acadyear/', acadyeartermviews.AcadYearListView.as_view(), name='acadyear-list'),
  path('acadyear/create/', acadyeartermviews.CreateAcadYear, name='acadyear-create'),
  path('acadyear/update/<int:pk>', acadyeartermviews.EditAcadYear, name='acadyear-update'),
  path('acadyear/delete/<int:pk>', acadyeartermviews.DeleteAcadYear.as_view(), name='acadyear-delete'),  

  # Class Section
  path('classsection/', classsectionviews.SectionListView.as_view(), name='classsection-list'),
  path('classsection/create/', classsectionviews.CreateClassSection, name='classsection-create'),
  path('classsection/update/<int:pk>', classsectionviews.EditClassSection, name='classsection-update'),
  path('classsection/delete/<int:pk>', classsectionviews.DeleteClassSection.as_view(), name='classsection-delete'),  

  # Subject
  path('subject/', subjectviews.SubjectListView.as_view(), name='subject-list'),
  path('subject/create/', subjectviews.CreateSubject, name='subject-create'),
  path('subject/update/<int:pk>', subjectviews.EditSubject, name='subject-update'),
  path('subject/delete/<int:pk>', subjectviews.DeleteSubject.as_view(), name='subject-delete'),  

  # Test Cycle
  path('testcycle/', testcycleviews.TestCycleListView.as_view(), name='testcycle-list'),
  path('testcycle/create/', testcycleviews.CreateTestCycle, name='testcycle-create'),
  path('testcycle/update/<int:pk>', testcycleviews.EditTestCycle, name='testcycle-update'),
  path('testcycle/delete/<int:pk>', testcycleviews.DeleteTestCycle.as_view(), name='testcycle-delete'),  

]