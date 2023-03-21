from django import forms
from django.forms.widgets import DateInput, Textarea
from django.forms import ModelForm
from django.db.models import Q
from apps.student.models import Student

class StudentForm(ModelForm):
    prefix = 'Student'

    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
            'date_of_admission': DateInput(attrs={'type': 'date'}),
            'address': Textarea(attrs={'rows': 2}),
            'others': Textarea(attrs={'rows': 2})
        }
    
    def __init__(self, student_id=None, **kwargs):
        self.studentId = student_id
        return super(StudentForm, self).__init__(**kwargs)


    def clean_registration_number(self):
        reg = self.cleaned_data.get('registration_number')
        existingregno = False
        try:
            st = Student.objects.get(registration_number=reg)
        except Student.DoesNotExist:
            # No other student using this registration no
            pass
        else:
            # if current student is not matching with that
            if (self.studentId != st.id): # for 'create' usage
                # There is already another student with this registration no
                raise forms.ValidationError('This registration number is already associated with another student.', code='unique')
            else: # for 'update' usage
                pass
        return reg