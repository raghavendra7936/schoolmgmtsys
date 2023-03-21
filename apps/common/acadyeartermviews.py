from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from apps.common.forms import AcademicYearForm
from apps.common.commondb import SchoolMgmtCommon
from django.views.generic import ListView, DeleteView
from apps.common.models import AcademicYear
from django.contrib import messages
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import render


class AcadYearListView(LoginRequiredMixin, ListView):
  model = AcademicYear
  template_name = 'common/acadyear_index.html'
  context_object_name = 'acadyear_list'

  def get_queryset(self):
      return SchoolMgmtCommon.GetAllAcadYears()

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['form'] = AcademicYearForm()
      return context

@login_required
def CreateAcadYear(request):
    if request.method == 'POST':
        acyear = request.POST.get("AcademicYear-academicyear")
        current = request.POST.get("AcademicYear-current")
        if (current == 'on'):
            isCurrent = True
        else:
            isCurrent = False
        form = AcademicYearForm(data=request.POST)
        if form.is_valid():
            if (isCurrent):
                AcademicYear.objects.filter(current=True).update(current=False)
            result = SchoolMgmtCommon.AddAcademicYear(acyear, isCurrent)
            return HttpResponseRedirect(reverse_lazy('acadyear-list'))
        else:
            messages.add_message(request, messages.ERROR, 'Academic Year is already existing')
            template_name = 'common/edit_form.html'
            return render(request, template_name, {
                'form': form,})

@login_required
def EditAcadYear(request, pk):
    template_name = 'common/edit_form.html'
    acyear = AcademicYear(**SchoolMgmtCommon.GetAcademicYear(pk)[0])
    if request.method == 'POST':
        current = request.POST.get("AcademicYear-current")
        if (current == 'on'):
            isCurrent = True
        else:
            isCurrent = False
        form = AcademicYearForm(instance=acyear, data=request.POST)    
        if form.is_valid():
            if (isCurrent):
               AcademicYear.objects.filter(current=True).update(current=False)
            form.save()
            return HttpResponseRedirect(reverse_lazy('acadyear-list'))
        else:
            errors = form.errors.as_data()
            if ('academicyear' in errors):
                ayError = errors['academicyear']
                ayErrorMsgs = ayError[0].messages
                if (not any("Duplicate academic year" in msg for msg in ayErrorMsgs)):
                    # ignore error
                    form.errors.clear()
                    if (isCurrent):
                        AcademicYear.objects.filter(current=True).update(current=False)
                        AcademicYear.objects.filter(id=pk).update(current=True)
                        messages.add_message(request, messages.SUCCESS, 'Updated academic year successfully')
                        return HttpResponseRedirect(reverse_lazy('acadyear-list'))
                    else:
                        messages.add_message(request, messages.WARNING, 'Nothing to save')
    else:
        form = AcademicYearForm(instance=acyear)
    return render(request, template_name, {
        'form': form,
    })

class DeleteAcadYear(LoginRequiredMixin, DeleteView):
    model = AcademicYear
    success_url = reverse_lazy('acadyear-list')
    template_name = 'common/confirm_delete.html'
    success_message = "The academic year {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, 'Cannot delete academic year as it is set to current')
            return HttpResponseRedirect(reverse_lazy('acadyear-list'))
        messages.success(self.request, self.success_message.format(obj.academicyear))
        return super(DeleteAcadYear, self).delete(request, *args, **kwargs)    