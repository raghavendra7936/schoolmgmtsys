from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from apps.common.models import ClassGrade, ClassSection
from django.views.generic import ListView, DeleteView
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from .models import Student
from .studentdb import SchoolMgmtStudent
from .forms import StudentForm


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'student/student_index.html'
    context_object_name = 'students'
    
    def get_queryset(self):
        studentslist = SchoolMgmtStudent.GetAllStudents()
        students = [Student(**st) for st in studentslist]
        return students

@login_required
def AddStudent(request):
    if request.method == 'POST':
        newStudent = { 
            'current_status': request.POST['Student-current_status'],
            'registration_number': request.POST['Student-registration_number'],
            'surname': request.POST['Student-surname'],
            'firstname': request.POST['Student-firstname'],
            'middle_name': request.POST['Student-middle_name'],
            'gender': request.POST['Student-gender'],
            'date_of_birth': request.POST['Student-date_of_birth'],
            'current_class': request.POST['Student-current_class'] if not '' else None,
            'current_section': request.POST['Student-current_section'] if not '' else None,
            'date_of_admission': request.POST['Student-date_of_admission'],
            'parent_mobile_number': request.POST['Student-parent_mobile_number'],
            'address': request.POST['Student-address'],
            'remarks': request.POST['Student-remarks'],
        }
        form = StudentForm(data=request.POST)
        if form.is_valid():
            result = SchoolMgmtStudent.AddStudent(newStudent)
            if (result):
                messages.add_message(request, messages.SUCCESS, 'Added new student successfully')
            else:
                messages.add_message(request, messages.ERROR, 'Error adding new student. Please try again')
            return HttpResponseRedirect(reverse_lazy('student-list'))
        else:
            messages.add_message(request, messages.ERROR, 'Registration number is already existing. Please check')
            template_name = 'student/student_addedit.html'
            return render(request, template_name, {
             'form': form,})
    else:
        form = StudentForm()
        return render(request, 'student/student_addedit.html', {
            'form': form, } )

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'student/student_detail.html'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        studentdetail = SchoolMgmtStudent.GetStudent(pk)
        student = Student(**studentdetail[0])
        return student

@login_required
def EditStudent(request, pk):
    template_name = 'student/student_addedit.html'
    studentdetail = SchoolMgmtStudent.GetStudent(pk)
    student = Student(**studentdetail[0])
    if request.method == 'POST':
        editStudent = { 
            'current_status': request.POST['Student-current_status'],
            'registration_number': request.POST['Student-registration_number'],
            'surname': request.POST['Student-surname'],
            'firstname': request.POST['Student-firstname'],
            'middle_name': request.POST['Student-middle_name'],
            'gender': request.POST['Student-gender'],
            'date_of_birth': request.POST['Student-date_of_birth'],
            'current_class': request.POST['Student-current_class'] if not '' else None,
            'current_section': request.POST['Student-current_section'] if not '' else None,
            'date_of_admission': request.POST['Student-date_of_admission'],
            'parent_mobile_number': request.POST['Student-parent_mobile_number'],
            'address': request.POST['Student-address'],
            'remarks': request.POST['Student-remarks'],
        }        
        form = StudentForm(instance=student, data=request.POST, student_id=pk)
        
        if form.is_valid():
            #form.save()
            SchoolMgmtStudent.UpdateStudent(editStudent, pk)
            return HttpResponseRedirect(reverse_lazy('student-list'))
        else:
            # if reg no is already in use and with current student, ignore
            errors = form.errors.as_data()
            if ('registration_number' in errors):
                regnoError = errors['registration_number']
                regnoErrorMsgs = regnoError[0].messages
                if (not any("This registration number is already associated" in msg for msg in regnoErrorMsgs)):
                    # ignore error
                    form.errors.clear()
                    SchoolMgmtStudent.UpdateStudent(editStudent, pk)
                    messages.add_message(request, messages.SUCCESS, 'Updated student record successfully')
                    return HttpResponseRedirect(reverse_lazy('student-list'))
    else:
        form = StudentForm(instance=student)
    return render(request, template_name, {
        'form': form, 'object': student
    })

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'common/confirm_delete.html'
    model = Student
    success_url = reverse_lazy('student-list')
