from apps.common.models import AcademicYear, ClassGrade, Subject, TestCycle
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DeleteView
from django.contrib import messages
from django.template import RequestContext
from apps.student.models import Student
from apps.result.models import Result
from apps.student.studentdb import SchoolMgmtStudent
from apps.common.commondb import SchoolMgmtCommon
from apps.result.resultdb import SchoolMgmtResult
from .forms import TCResultForm
from .tcfilter import TestCycleFilter


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'result/studentresult_index.html'
    context_object_name = 'students'
    
    def get_queryset(self):
        studentslist = SchoolMgmtStudent.GetAllStudents()
        students = [Student(**st) for st in studentslist]
        return students

@login_required        
def ShowTestCycleResults(request, stid):
    if request.method == 'GET':
        if('name' in request.GET):
            tc = request.GET['name']
        else:
            alltc = TestCycle.objects.all()
            if(not alltc):
                messages.add_message(request, messages.ERROR, 'Please add a test cycle first')
                return HttpResponseRedirect(reverse('testcycle-list'))
            else:
                tc = alltc[0].id
    stresults = SchoolMgmtResult.GetStudentTestCycleResult(stid, tc, request.current_acyear_id)
    tcresults = [Result(**r) for r in stresults]
    tcycles = SchoolMgmtCommon.GetAllTestCycles()
    testcycles = TestCycle.objects.all()
    tcfilter = TestCycleFilter(request.GET)
    newresult = Result()
    stobj = Student.objects.get(id=stid)
    tcobj = TestCycle.objects.get(id=tc)
    newresult.student = stobj
    newresult.testcycle = tcobj
    newresult.current_class = stobj.current_class
    newresult.academicyear = AcademicYear.objects.get(id=request.current_acyear_id)
    totalmaxmarks = sum(tc.max_marks for tc in tcresults)
    totalstudentscore = sum(tc.student_score for tc in tcresults)
    if (totalmaxmarks):
        pct = round(totalstudentscore*100/totalmaxmarks, 2)
    else:
        pct = 0
    tcresultform = TCResultForm(instance=newresult)
    return render(request, 'result/student_tcresultfilter_index.html', {
        'tcresult': tcresults, 'filter': tcfilter, 'tcform': tcresultform, 'student': stobj, 'testcycle': tcobj,
        'totalmaxmarks': totalmaxmarks, 'totalstudentscore': totalstudentscore, 'percent': pct
    })

@login_required
def CreateTestResult(request, stid):
    if request.method == 'POST':
        form = TCResultForm(data=request.POST)
        tcresult = { 
            'studentid': request.POST['TCResult-student'],
            'academicyear': request.POST['TCResult-academicyear'],
            'current_class': request.POST['TCResult-current_class'],
            'subject': request.POST['TCResult-subject'],
            'testcycle': request.POST['TCResult-testcycle'],
            'max_marks': request.POST['TCResult-max_marks'],
            'student_score': request.POST['TCResult-student_score']
        }
        studenttcresult = Result()
        studenttcresult.student = Student.objects.get(id=stid)
        studenttcresult.academicyear = AcademicYear.objects.get(id=request.POST['TCResult-academicyear'])
        studenttcresult.current_class = ClassGrade.objects.get(id=request.POST['TCResult-current_class'])
        studenttcresult.subject = Subject.objects.get(id=request.POST['TCResult-subject'])
        studenttcresult.testcycle = TestCycle.objects.get(id=request.POST['TCResult-testcycle'])
        if form.is_valid():
            result = SchoolMgmtResult.AddTestCycleResult(tcresult)
            messages.add_message(request, messages.SUCCESS, 'Added new result succesfully')
            return HttpResponseRedirect(reverse_lazy('result-viewstudentresult', kwargs={'stid': stid}))
        else:
            messages.add_message(request, messages.ERROR, 'Error when adding record')
            template_name = 'result/tcresult_edit.html'
            return render(request, template_name, {
                'form': form, 'tcresult': studenttcresult, 'title': 'Edit Result'})

class StudentTestCycleResultListView(LoginRequiredMixin, ListView):
  model = Result
  template_name = 'result/student_tcresultfilter_index.html'

  def get_queryset(self):
      stresults = SchoolMgmtResult.GetStudentTestCycleResult()
      tcresults = [Result(**r) for r in stresults]
      return tcresults
  
  def get_context_data(self, **kwargs):
        context = super(StudentTestCycleResultListView, self).get_context_data(**kwargs)
        context['testcycles'] = self.get_queryset_testcycles()
        return context
  
  def get_queryset_testcycles(self):
      tcycles = SchoolMgmtCommon.GetAllTestCycles()
      testcycles = [TestCycle(*t) for t in tcycles]
      return testcycles

@login_required
def EditTCResult(request, pk):
    template_name = 'result/tcresult_edit.html'
    tcresult = Result(**SchoolMgmtResult.GetSingleTCResult(pk)[0])
    if request.method == 'POST':
        form = TCResultForm(instance=tcresult, data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Updated result succesfully')
            return HttpResponseRedirect(reverse('result-viewstudentresult', kwargs={'stid': tcresult.student.id}))
    else:
        print (request.GET)
        # from add result screen
        form = TCResultForm(instance=tcresult)
    return render(request, template_name, {
        'form': form, 'tcresult': tcresult, 'title': 'Edit Result'
    })


class DeleteTestResult(LoginRequiredMixin, DeleteView):
    model = Result
    template_name = 'common/confirm_delete.html'
    success_message = "The test result {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        self.success_url = reverse('result-viewstudentresult', kwargs={'stid': obj.student.id})
        messages.success(self.request, self.success_message.format(obj))
        return super(DeleteTestResult, self).delete(request, *args, **kwargs)

