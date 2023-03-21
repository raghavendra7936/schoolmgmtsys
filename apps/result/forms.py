from django import forms
from django.forms import ModelForm
from .models import Result

class TCResultForm(ModelForm):
  prefix = 'TCResult'
  
  class Meta:
    model = Result
    fields = '__all__'
    widgets = {
      'student': forms.HiddenInput(), 
      'testcycle': forms.HiddenInput(),
      'current_class': forms.HiddenInput(),
      'academicyear': forms.HiddenInput()
    }

  def clean(self):
    data = self.cleaned_data
    maxmarks = data['max_marks']
    studentscore = data['student_score']
    if (studentscore > maxmarks):
      raise forms.ValidationError({'student_score': ["Student score is more than maximum marks",]}, code="Range")
