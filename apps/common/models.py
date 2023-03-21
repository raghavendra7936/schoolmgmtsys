from django.db import models

# Create your models here.
class ClassGrade(models.Model):
  """ Class/Grade """
  grade = models.CharField(max_length=10, unique=True)

  class Meta:
    verbose_name = "Grade"
    verbose_name_plural = "Grades"
    ordering = ['grade']

  def __str__(self):
    return self.grade

class ClassSection(models.Model):
  """ Class Section """
  sectionname = models.CharField(max_length=1, unique=True)

  class Meta:
    verbose_name = "Section"
    verbose_name_plural = "Sections"
    ordering = ['sectionname']

  def __str__(self):
    return self.sectionname

class AcademicYear(models.Model):
  """ Academic year """
  academicyear = models.CharField(max_length=200, unique=True)
  current = models.BooleanField(default=True)

  class Meta:
    verbose_name = "AcademicYear"
    verbose_name_plural = "AcademicYears"    
    ordering = ['academicyear']

  def __str__(self):
    return self.academicyear

class Subject(models.Model):
  """ Subject """
  name = models.CharField(max_length=200, unique=True)

  class Meta:
    ordering = ['name']

  def __str__(self):
    return self.name

class TestCycle(models.Model):
  """ Test Cycle """
  name = models.CharField(max_length=200, unique=True)

  class Meta:
    ordering = ['name']

  def __str__(self):
    return self.name