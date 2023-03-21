from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.staff.forms import StaffForm
from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from .models import Staff
from .staffdb import SchoolMgmtStaff

class StaffListView(LoginRequiredMixin, ListView):
    model = Staff
    template_name = 'staff/staff_index.html'
    context_object_name = 'staffs'
    
    def get_queryset(self):
        stafflist = SchoolMgmtStaff.GetAllStaffs()
        staffs = [Staff(**st) for st in stafflist]
        return staffs

@login_required
def AddStaff(request):
    if request.method == 'POST':
        newStaff = { 
            'current_status': request.POST['Staff-current_status'],
            'registration_number': request.POST['Staff-registration_number'],
            'surname': request.POST['Staff-surname'],
            'firstname': request.POST['Staff-firstname'],
            'middle_name': request.POST['Staff-middle_name'],
            'gender': request.POST['Staff-gender'],
            'date_of_birth': request.POST['Staff-date_of_birth'],
            'date_of_joining': request.POST['Staff-date_of_joining'],
            'mobile_number': request.POST['Staff-mobile_number'],
            'address': request.POST['Staff-address'],
            'remarks': request.POST['Staff-remarks'],
        }
        form = StaffForm(data=request.POST)
        if form.is_valid():
            result = SchoolMgmtStaff.AddStaff(newStaff)
            if (result):
                messages.add_message(request, messages.SUCCESS, 'Added new staff successfully')
            else:
                messages.add_message(request, messages.ERROR, 'Error adding new staff. Please try again')
            return HttpResponseRedirect(reverse_lazy('staff-list'))
        else:
            messages.add_message(request, messages.ERROR, 'Registration number is already existing. Please check')
            template_name = 'staff/staff_addedit.html'
            return render(request, template_name, {
             'form': form,})
    else:
        form = StaffForm()
        return render(request, 'staff/staff_addedit.html', {
            'form': form, } )

class StaffDetailView(LoginRequiredMixin, DetailView):
    model = Staff
    template_name = 'staff/staff_detail.html'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        staffdetail = SchoolMgmtStaff.GetStaff(pk)
        staff = Staff(**staffdetail[0])
        return staff

@login_required
def EditStaff(request, pk):
    template_name = 'student/student_addedit.html'
    staffdetail = SchoolMgmtStaff.GetStaff(pk)
    currentstaff = Staff(**staffdetail[0])
    if request.method == 'POST':
        editStaff = { 
            'current_status': request.POST['Staff-current_status'],
            'registration_number': request.POST['Staff-registration_number'],
            'surname': request.POST['Staff-surname'],
            'firstname': request.POST['Staff-firstname'],
            'middle_name': request.POST['Staff-middle_name'],
            'gender': request.POST['Staff-gender'],
            'date_of_birth': request.POST['Staff-date_of_birth'],
            'date_of_joining': request.POST['Staff-date_of_joining'],
            'mobile_number': request.POST['Staff-mobile_number'],
            'address': request.POST['Staff-address'],
            'remarks': request.POST['Staff-remarks'],
        }        
        form = StaffForm(instance=currentstaff, data=request.POST, staff_id=pk)
        
        if form.is_valid():
            #form.save()
            SchoolMgmtStaff.UpdateStaff(editStaff, pk)
            return HttpResponseRedirect(reverse_lazy('staff-list'))
        else:
            # if reg no is already in use and with current student, ignore
            errors = form.errors.as_data()
            if ('registration_number' in errors):
                regnoError = errors['registration_number']
                regnoErrorMsgs = regnoError[0].messages
                if (not any("This registration number is already associated" in msg for msg in regnoErrorMsgs)):
                    # ignore error
                    form.errors.clear()
                    SchoolMgmtStaff.UpdateStaff(editStaff, pk)
                    messages.add_message(request, messages.SUCCESS, 'Updated staff record successfully')
                    return HttpResponseRedirect(reverse_lazy('staff-list'))
    else:
        form = StaffForm(instance=currentstaff)
    return render(request, template_name, {
        'form': form, 'object': currentstaff
    })


class StaffDeleteView(LoginRequiredMixin, DeleteView):
  model = Staff
  success_message = "Successfully deleted staff member"
  success_url = reverse_lazy('staff-list')