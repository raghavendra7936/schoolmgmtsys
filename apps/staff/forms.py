from django import forms
from django.forms.widgets import DateInput, Textarea
from django.forms import ModelForm
from apps.staff.models import Staff

class StaffForm(ModelForm):
    prefix = 'Staff'

    class Meta:
        model = Staff
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
            'date_of_joining': DateInput(attrs={'type': 'date'}),
            'address': Textarea(attrs={'rows': 2}),
            'remarks': Textarea(attrs={'rows': 2})
        }
    
    def __init__(self, staff_id=None, **kwargs):
        self.staffid = staff_id
        return super(StaffForm, self).__init__(**kwargs)


    def clean_registration_number(self):
        reg = self.cleaned_data.get('registration_number')
        existingregno = False
        try:
            st = Staff.objects.get(registration_number=reg)
        except Staff.DoesNotExist:
            # No other student using this registration no
            pass
        else:
            # if current student is not matching with that
            if (self.staffid != st.id): # for 'create' usage
                # There is already another student with this registration no
                raise forms.ValidationError('This registration number is already associated with another staff.', code='unique')
            else: # for 'update' usage
                pass
        return reg