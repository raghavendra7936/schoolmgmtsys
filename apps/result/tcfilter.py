import django_filters

from apps.common.models import TestCycle

class TestCycleFilter(django_filters.FilterSet):
	name = django_filters.ModelChoiceFilter(queryset=TestCycle.objects.all())

	class Meta:
		model = TestCycle
		fields = ['name']

