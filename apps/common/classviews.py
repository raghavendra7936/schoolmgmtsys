from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import request
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView, DeleteView
from apps.common.forms import ClassGradeForm
from apps.common.models import ClassGrade
from apps.common.commondb import SchoolMgmtCommon
from django.urls import reverse_lazy
from django.shortcuts import render

class ClassGradeListView(LoginRequiredMixin, ListView):
  model = ClassGrade
  template_name = 'common/class_index.html'
  context_object_name = 'class_list'

  def get_queryset(self):
      return SchoolMgmtCommon.GetAllClassGrades()

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['form'] = ClassGradeForm()
      return context

@login_required
def CreateClassGrade(request):
    if request.method == 'POST':
        gr = request.POST.get("Grade-grade")
        form = ClassGradeForm(data=request.POST)
        if form.is_valid():
            result = SchoolMgmtCommon.AddClassGrade(gr)
            if (result):
                messages.add_message(request, messages.SUCCESS, 'Added new class grade successfully')
            else:
                messages.add_message(request, messages.ERROR, 'Error adding class grade. Please try again')              
            return HttpResponseRedirect(reverse_lazy('class-list'))
        else:
            messages.add_message(request, messages.ERROR, 'Grade is already existing')
            template_name = 'common/edit_form.html'
            return render(request, template_name, {
                'form': form,})
        
@login_required
def EditClassGrade(request, pk):
    template_name = 'common/edit_form.html'
    classgrade = ClassGrade(**SchoolMgmtCommon.GetClassGrade(pk)[0])
    if request.method == 'POST':
        form = ClassGradeForm(instance=classgrade, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('class-list') )
    else:
        form = ClassGradeForm(instance=classgrade)
    return render(request, template_name, {
        'form': form,
    })

class DeleteClassGrade(LoginRequiredMixin, DeleteView):
    model = ClassGrade
    success_url = reverse_lazy('class-list')
    template_name = 'common/confirm_delete.html'
    success_message = "The class {} has been deleted with all its attached content"


