from apps.common.models import AcademicYear

def current_acadyear(request):
  try:
    current_acyear = AcademicYear.objects.get(current=True)
    contexts = {
        "current_acyear_id": current_acyear.id,
        "current_acyear": current_acyear.academicyear,
    }
  except AcademicYear.DoesNotExist:
    contexts = {}
  return contexts