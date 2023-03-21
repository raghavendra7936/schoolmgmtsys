from django.forms import inlineformset_factory, modelformset_factory
from django.forms.models import ModelForm
from django.forms.widgets import DateInput
from apps.common.models import AcademicYear, ClassGrade
from .models import Invoice, InvoiceItem, Receipt


class ReceiptForm(ModelForm):

    class Meta:
        model = Receipt
        fields = ['amount_paid', 'date_paid', 'comment']
        widgets = {
            'date_paid': DateInput(attrs={'type': 'date'}),
        }


InvoiceItemFormset = inlineformset_factory(
    Invoice, InvoiceItem, fields=['description', 'amount'], extra=1, can_delete=True)

InvoiceReceiptFormSet = inlineformset_factory(
    Invoice, Receipt, fields=('amount_paid', 'date_paid', 'comment'), extra=0, can_delete=True, form=ReceiptForm,
)

Invoices = modelformset_factory(Invoice, exclude=(), extra=4)

