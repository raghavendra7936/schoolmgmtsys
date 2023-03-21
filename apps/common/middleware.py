from .models import AcademicYear

class SchoolMgmtSiteConfig:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            current_acyear = AcademicYear.objects.get(current=True)
            request.current_acyear = current_acyear.academicyear
            request.current_acyear_id = current_acyear.id
        except AcademicYear.DoesNotExist:
            pass
        response = self.get_response(request)
        return response