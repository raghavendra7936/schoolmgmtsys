from django import forms
from django.forms import ModelForm
from apps.common.models import ClassGrade, AcademicYear, ClassSection, Subject, TestCycle

class ClassGradeForm(ModelForm):
  prefix = 'Grade'
  
  class Meta:
    model = ClassGrade
    fields = ['grade']

class ClassSectionForm(ModelForm):
  prefix = 'ClassSection'

  class Meta:
    model = ClassSection
    fields = ['sectionname']

class AcademicYearForm(ModelForm):
  prefix = 'AcademicYear'

  def __init__(self, *args, **kwargs):
      super(AcademicYearForm, self).__init__(*args, **kwargs)
      self.fields['current'].required = False

  class Meta:
    model = AcademicYear
    fields = ['academicyear', 'current']

    def clean_academicyear(self):
        ay = self.cleaned_data.get('academicyear')
        try:
            st = AcademicYear.objects.get(academicyear=ay)
        except AcademicYear.DoesNotExist:
            # No other student using this registration no
            pass
        else:
            # if current student is not matching with that
            if (self.id != st.id): # for 'create' usage
                # There is already another student with this registration no
                raise forms.ValidationError('Duplicate Academic year.', code='unique')
            else: # for 'update' usage
                pass
        return ay

class SubjectForm(ModelForm):
  prefix = 'Subject'

  class Meta:
    model = Subject
    fields = ['name']

class TestCycleForm(ModelForm):
  prefix = 'TestCycle'

  class Meta:
    model = TestCycle
    fields = ['name']