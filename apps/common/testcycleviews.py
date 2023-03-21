from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from apps.common.models import TestCycle
from apps.common.forms import TestCycleForm
from apps.common.commondb import SchoolMgmtCommon
from django.views.generic import ListView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import render


class TestCycleListView(LoginRequiredMixin, ListView):
  model = TestCycle
  template_name = 'common/testcycle_index.html'
  context_object_name = 'testcycle_list'

  def get_queryset(self):
      return SchoolMgmtCommon.GetAllTestCycles()

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['form'] = TestCycleForm()
      return context

@login_required
def CreateTestCycle(request):
    if request.method == 'POST':
        cyclename = request.POST.get("TestCycle-name")
        form = TestCycleForm(data=request.POST)
        if form.is_valid():
            result = SchoolMgmtCommon.AddTestCycle(cyclename)
            return HttpResponseRedirect(reverse_lazy('testcycle-list'))
        else:
            messages.add_message(request, messages.ERROR, 'Test Cycle is already existing')
            template_name = 'common/edit_form.html'
            return render(request, template_name, {
                'form': form,})

@login_required
def EditTestCycle(request, pk):
    template_name = 'common/edit_form.html'
    tc = TestCycle(**SchoolMgmtCommon.GetTestCycle(pk)[0])
    if request.method == 'POST':
        form = TestCycleForm(instance=tc, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('testcycle-list'))
    else:
        form = TestCycleForm(instance=tc)
    return render(request, template_name, {
        'form': form,
    })

class DeleteTestCycle(LoginRequiredMixin, DeleteView):
    model = TestCycle
    success_url = reverse_lazy('testcycle-list')
    template_name = 'common/confirm_delete.html'
    success_message = "The Test cycle {} has been deleted with all its attached content"

