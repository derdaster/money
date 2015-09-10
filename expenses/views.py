from __future__ import unicode_literals
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.db.models.fields.files import FieldFile
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.generic.base import TemplateView

from expenses.models import Expenses

from .forms import ContactForm, FilesForm, ContactFormSet

# def index(request):
#     # This view is missing all form handling logic for simplicity of the example
#     return render(request, 'expenses/index.html', {'form': MessageForm()})
class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, 'dummy.txt')

# class IndexView(generic.ListView):
#     template_name = 'expenses/index.html'
#     context_object_name = 'latest_expenses_list'
#    
#     def get_queryset(self):
#         """Return the last five added expenses."""
#         return Expenses.objects.order_by('-date')[:5]

    
class IndexView(TemplateView):
    template_name = 'demo/home.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        messages.info(self.request, 'This is a demo of a message.')
        return context
    
# def index(request):
#     return HttpResponse("Hello, world. You're at the poll index.")

class DetailView(generic.DetailView):
    model = Expenses
    template_name = 'expenses/detail.html'


class ResultsView(generic.DetailView):
    model = Expenses
    template_name = 'expenses/results.html'
    
def detail(request, expenses_id):
    expense = get_object_or_404(Expenses, pk=expenses_id)
    return render(request, 'expenses/detail.html', {'expense': expense})

def results(request, expenses_id):
    expense = get_object_or_404(Expenses, pk=expenses_id)
    return render(request, 'expenses/results.html', {'expense': expense})


# Create your views here.
