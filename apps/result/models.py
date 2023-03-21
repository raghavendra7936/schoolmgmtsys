from django.db import models
from apps.common.models import AcademicYear, ClassGrade, TestCycle, Subject
from apps.student.models import Student

# Create your models here.

class Result(models.Model):
   student = models.ForeignKey(Student, on_delete=models.CASCADE)
   academicyear = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
   current_class = models.ForeignKey(ClassGrade, on_delete=models.CASCADE)
   subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
   testcycle = models.ForeignKey(TestCycle, on_delete=models.CASCADE)
   max_marks = models.IntegerField(default=0)
   student_score = models.IntegerField(default=0)

   class Meta:
     ordering = ['subject']

   def __str__(self):
     return f'{self.student} {self.academicyear} {self.current_class} {self.testcycle} {self.subject}'