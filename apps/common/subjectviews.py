from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from apps.common.models import Subject
from apps.common.forms import AcademicYearForm, ClassSectionForm, SubjectForm
from apps.common.commondb import SchoolMgmtCommon
from django.views.generic import ListView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import render


class SubjectListView(LoginRequiredMixin, ListView):
  model = Subject
  template_name = 'common/subject_index.html'
  context_object_name = 'subject_list'

  def get_queryset(self):
      return SchoolMgmtCommon.GetAllSubjects()

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['form'] = SubjectForm()
      return context

@login_required
def CreateSubject(request):
    if request.method == 'POST':
        subj = request.POST.get("Subject-name")
        form = SubjectForm(data=request.POST)
        if form.is_valid():
            result = SchoolMgmtCommon.AddSubject(subj)
            if (result):
                messages.add_message(request, messages.SUCCESS, 'Added new subject successfully')
            else:
                messages.add_message(request, messages.ERROR, 'Error adding subject. Please try again')            
            return HttpResponseRedirect(reverse_lazy('subject-list'))
        else:
            form_error = True

@login_required
def EditSubject(request, pk):
    template_name = 'common/edit_form.html'
    subj = Subject(**SchoolMgmtCommon.GetSubject(pk)[0])
    if request.method == 'POST':
        form = SubjectForm(instance=subj, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('subject-list'))
    else:
        form = SubjectForm(instance=subj)
    return render(request, template_name, {
        'form': form,
    })

class DeleteSubject(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy('subject-list')
    template_name = 'common/confirm_delete.html'
    success_message = "The subject {} has been deleted with all its attached content"
