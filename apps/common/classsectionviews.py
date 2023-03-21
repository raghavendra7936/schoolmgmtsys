from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from apps.common.forms import AcademicYearForm, ClassSectionForm
from apps.common.commondb import SchoolMgmtCommon
from django.views.generic import ListView, DeleteView
from apps.common.models import ClassSection
from django.contrib import messages
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import render


class SectionListView(LoginRequiredMixin, ListView):
  model = ClassSection
  template_name = 'common/classsection_index.html'
  context_object_name = 'classsection_list'

  def get_queryset(self):
      return SchoolMgmtCommon.GetAllClassSections()

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['form'] = ClassSectionForm()
      return context

@login_required
def CreateClassSection(request):
    if request.method == 'POST':
        section = request.POST.get("ClassSection-sectionname")
        form = ClassSectionForm(data=request.POST)
        if form.is_valid():
            result = SchoolMgmtCommon.AddClassSection(section)
            if (result):
                messages.add_message(request, messages.SUCCESS, 'Added new class section successfully')
            else:
                messages.add_message(request, messages.ERROR, 'Error adding class section. Please try again')            
            return HttpResponseRedirect(reverse_lazy('classsection-list'))
        else:
            form_error = True

@login_required
def EditClassSection(request, pk):
    template_name = 'common/edit_form.html'
    classsection = ClassSection(**SchoolMgmtCommon.GetClassSection(pk)[0])
    if request.method == 'POST':
        form = ClassSection(instance=classsection, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('classsection-list'))
    else:
        form = ClassSectionForm(instance=classsection)
    return render(request, template_name, {
        'form': form,
    })

class DeleteClassSection(LoginRequiredMixin, DeleteView):
    model = ClassSection
    success_url = reverse_lazy('classsection-list')
    template_name = 'common/confirm_delete.html'
    success_message = "The class section {} has been deleted with all its attached content"