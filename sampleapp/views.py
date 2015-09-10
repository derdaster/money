# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from datetime import timedelta
import sys

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models.aggregates import Sum
from django.db.models.constants import LOOKUP_SEP
from django.db.models.fields.files import FieldFile
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.template.context import RequestContext
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from sampleapp.forms import EditExpenseForm, IncomeForm, IncomeFilterForm, EditAccountForm, EditIncomeForm
from expenses.models import Expenses, Accounts, Contractors, Budget, Category, Subcategory, Income

from .forms import ContactForm, FilesForm, ContactFormSet, BudgetUser, AccountForm, ExpenseForm, AccuserForm, BudgetForm, ContractorForm, CategoryForm, SubcategoryForm, LoginForm, LogoutForm, ExpenseFilterForm


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
    template_name = 'demo/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context
    

    
# def index(request):
#     return HttpResponse("Hello, world. You're at the poll index.")
class LoggedView(TemplateView):
    template_name = 'demo/home.html'
    def get_context_data(self, **kwargs):
        context = super(LoggedView, self).get_context_data(**kwargs)
        messages.info(self.request, 'Witaj ' + self.request.user.username)
        return context
class DetailView(generic.DetailView):
    model = Expenses
    template_name = 'expenses/detail.html'


class ResultsView(generic.DetailView):
    model = Expenses
    template_name = 'expenses/results.html'
    
class FormHorizontalView(FormView):
    form_class = ContactForm
    template_name = 'demo/form_horizontal.html'
    
class AddUserView(FormView):
    form_class = ContactForm
    template_name = 'demo/add_user.html'
       
class AddBudgetView(FormView):
    form_class = BudgetForm
    template_name = 'demo/add_budget.html' 
    
class AddBudgetUserView(FormView):
    form_class = BudgetUser
    template_name = 'demo/add_budgetuser.html'
    
class AddAccountView(FormView):
    form_class = AccountForm
    template_name = 'demo/add_account.html'
    
class AddExpenseView(FormView):
    form_class = ExpenseForm
    template_name = 'demo/add_expense.html'

# class ExpenseFilterView(FormView):
#     form_class = ExpenseFilterForm()
#     template_name = 'demo/filter_expenses.html'
    
class AddAccuserView(FormView):
    form_class = AccuserForm
    template_name = 'demo/add_accuser.html'
    
class AddContractorView(FormView):
    form_class = ContractorForm
    template_name = 'demo/add_contractor.html'

class AddCategoryView(FormView):
    form_class = CategoryForm
    template_name = 'demo/add_category.html'
    
# class AddSubcategoryView(FormView):
#     form_class = SubcategoryForm
#     template_name = 'demo/add_subcategory.html'
    
class AddLoginView(FormView):
    form_class = LoginForm
    template_name = 'demo/add_login.html'
    
class AddLogoutView(FormView):
    form_class = LogoutForm
    template_name = 'demo/logout.html'   
def detail(request, expenses_id):
    expense = get_object_or_404(Expenses, pk=expenses_id)
    return render(request, 'expenses/detail.html', {'expense': expense})

def results(request, expenses_id):
    expense = get_object_or_404(Expenses, pk=expenses_id)
    return render(request, 'expenses/results.html', {'expense': expense})

def submitForm(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = request.POST['name']
            surname = request.POST['surname']
            nickname = request.POST['nickname']
            password = request.POST['password']
            email = request.POST['email']
#             user = Users(name=name, surname=surname, nickname=nickname, password=password)
            user = User.objects.create_user(username=nickname, email=email, password=password)
            user.first_name = name
            user.last_name = surname
            user.save()
            b = Budget(name=user.username + '_budget')
            b.save()
            b.members.add(user)
            u = Accounts(name='konto', amount=0)
            u.save()
            u.members.add(user)
            messages.info(request, 'Zarejestrowano użytkownika, teraz możesz zalogować się w panelu logowania')
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    return render(request, 'demo/add_user.html', {'form': form})
def submitBudget(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BudgetForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = request.POST['name']
            user = Budget(name=name)
            user.save()
            user.members.add(request.user)
            flush_transaction()
            messages.info(request, 'Dodano nowy budżet')
            return HttpResponseRedirect('submitBudget')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BudgetForm()
        
    return render(request, 'demo/add_budget.html', {'form': form})

def submitBudgetUser(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BudgetUser(request.POST, user_id=request.user)
        # check whether it's valid:
        if form.is_valid():
            name = request.POST['name']
            budget = request.POST['budget']
            b = Budget.objects.get(id=budget)
            u = User.objects.get(username=name)
            u.save()
            b.members.add(u)
            b.save()
            flush_transaction()
            messages.info(request, 'Dodano członka budżetu')
            return HttpResponseRedirect('submitBudgetUser')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BudgetUser(user_id=request.user)

    return render(request, 'demo/add_budgetuser.html', {'form': form})
def submitAccount(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AccountForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = request.POST['name']
            bankName = request.POST['bank_Name']
            comment = request.POST['comment']
            accountNumber = 0
            if 'account_Number' in request.POST:
                if request.POST['account_Number'] > 0:
                    accountNumber = request.POST['account_Number']
            accountState = request.POST['account_State']
            u = Accounts(name=name, bankName=bankName, comment=comment, number=accountNumber, amount=accountState)
            u.save()
            u.members.add(request.user)
            flush_transaction()
            messages.info(request, 'Dodano nowe konto')
            return HttpResponseRedirect('submiAccount')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AccountForm()

    return render(request, 'demo/add_account.html', {'form': form})

def submitExpense(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ExpenseForm(request.POST, user_id=request.user)
        # check whether it's valid:
        if form.is_valid():
            name = request.POST['name']
            date = request.POST['date']
            amount = request.POST['amount']
            accountNumber = request.POST['account']
            contractor = request.POST['contractor']
            fixed = False
            closed = False
            if 'fixed' in request.POST:
                fixed = request.POST['fixed']
            if 'closed' in request.POST:
                closed = request.POST['closed']
            a = Accounts.objects.get(id=accountNumber)
            u = Expenses(name=name, date=date, amount=amount, user=request.user, account=Accounts.objects.get(id=accountNumber), fixed=fixed, closed=closed, contractor=Contractors.objects.get(id=contractor))
            if 'subcategory' in request.POST:
                subcategory = request.POST['subcategory']
                u = Expenses(name=name, date=date, amount=amount, user=request.user, account=Accounts.objects.get(id=accountNumber), fixed=fixed, closed=closed, subcategory=Subcategory.objects.get(id=subcategory), contractor=Contractors.objects.get(id=contractor))
            u.save()
            a.amount = a.amount - float(amount)
            a.save()
            flush_transaction()
            messages.info(request, 'Dodano wydatek')
            if(a.amount < 0):
                messages.error(request, 'Dodałeś wydatek, któy spowodował że jesteś na debecie!')
            return HttpResponseRedirect('submitExpense')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ExpenseForm(user_id=request.user)

    return render(request, 'demo/add_expense.html', {'form': form})
def submitIncome(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = IncomeForm(request.POST, user_id=request.user)
        # check whether it's valid:
        if form.is_valid():
            name = request.POST['name']
            date = request.POST['date']
            amount = request.POST['amount']
            accountNumber = request.POST['account']
            fixed = False
            a = Accounts.objects.get(id=accountNumber)
            u = Income(name=name, date=date, amount=amount, user=request.user, account=Accounts.objects.get(id=accountNumber), fixed=fixed)
            u.save()
            a.amount = a.amount + float(amount)
            a.save()
            flush_transaction()
            messages.info(request, 'Dodano przychód')
            return HttpResponseRedirect('submitIncome')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = IncomeForm(user_id=request.user)

    return render(request, 'demo/add_income.html', {'form': form})
def submitAccuser(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AccuserForm(request.POST, user_id=request.user)
        # check whether it's valid:
        if form.is_valid():
            name = request.POST['name']
            user = request.POST['users2']
            a = Accounts.objects.get(id=name)
            a.save()
            u = User.objects.get(id=user)
            a.save()
            a.members.add(u)
            a.save()

            flush_transaction()
            messages.info(request, 'Dodano użytkownika konta')
            return HttpResponseRedirect('submitAccuser')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AccuserForm(user_id=request.user)

    return render(request, 'demo/add_accuser.html', {'form': form})
def submitContractor(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContractorForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = request.POST['name']
            for obj in Budget.objects.filter(members=request.user):
                c = Contractors(name=name, budget=obj)
                c.save()


            flush_transaction()
            messages.info(request, 'Dodano kontrahenta')
            return HttpResponseRedirect('submitContractor')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContractorForm()

    return render(request, 'demo/add_contractor.html', {'form': form})

def submitCategory(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CategoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = request.POST['name']
            for obj in Budget.objects.filter(members=request.user):
                c = Category(name=name, limit=0, budget=obj)
                c.save()
            
            flush_transaction()
            messages.info(request, 'Dodano kategorię')
            return HttpResponseRedirect('submitCategory')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CategoryForm()

    return render(request, 'demo/add_category.html', {'form': form})

def submitSubcategory(request):
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, user_id=request.user)
        if form.is_valid():
            category = request.POST['category']
            
            cat = Category.objects.get(id=category)
            cat.save()
            name = request.POST['name']
            for obj in Budget.objects.filter(members=request.user):
                c = Subcategory(name=name, category=cat, budget=obj)
                c.save()
            messages.info(request, 'Dodano podkategorię')
            return HttpResponseRedirect('submitSubcategory')
    else:
        form = SubcategoryForm(user_id=request.user)
    return render(request, 'demo/add_subcategory.html', {'form': form})

def submitLogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect("/home/")
    else:
        # Show an error page
        form = LoginForm()
            
            
    return render(request, 'demo/add_login.html', {'form': form, })
def logOut(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")

def getExpenses(request):
    form = AddExpenseView()
    latest_poll_list = Expenses.objects.filter()
    expenses_sum = Expenses.objects.filter().aggregate(Sum('amount'))
    template = loader.get_template('demo/expenses.html')
    context = RequestContext(request, {'form': form,
        'latest_poll_list': latest_poll_list, 'expenses_sum': expenses_sum,
    })
    return HttpResponse(template.render(context))
def viewExpenses(request):
    # if this is a POST request we need to process the form data
    latest_poll_list = Expenses.objects.filter(user__in=User.objects.filter(id=request.user.id))
    expenses_sum = latest_poll_list.aggregate(Sum('amount'))
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ExpenseFilterForm(request.POST, user_id=request.user)
        # check whether it's valid:
        if form.is_valid():
            name = request.POST['name']
            date_from = request.POST['date_from']
            date_to = request.POST['date_to']
            user = request.POST['user']
            account = request.POST['account']
            contractor = request.POST['contractor']
            category = request.POST['category']
            if 'closed' in request.POST:
                closed = request.POST['closed']
                if closed == 'Tak':
                    closed = True
                else:
                    closed = False
            if name:
                latest_poll_list = latest_poll_list.filter(name__contains=name)
            if int(user) != 0:
                latest_poll_list = latest_poll_list.filter(user=User.objects.get(id=user))
            if int(account) != 0:
                print(Accounts.objects.get(id=account).name)
                latest_poll_list = latest_poll_list.filter(account=Accounts.objects.get(id=account))
                print(latest_poll_list)
            if int(contractor) != 0:
                latest_poll_list = latest_poll_list.filter(contractor=contractor)
            if int(category) != 0:
                latest_poll_list = latest_poll_list.filter(subcategory__in=Subcategory.objects.filter(id__in=Category.objects.filter(id=category).values('subcategory')))
            if date_from:
                latest_poll_list = latest_poll_list.filter(date__gte=date_from)
            if date_to:
                latest_poll_list = latest_poll_list.filter(date__lte=date_to)
            if closed:
                latest_poll_list = latest_poll_list.filter(closed=closed)     
            print(date_from)
            expenses_sum = latest_poll_list.aggregate(Sum('amount'))
            return render(request, 'demo/view_expenses.html', {'form': form,
        'latest_poll_list': latest_poll_list, 'expenses_sum': expenses_sum, })

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ExpenseFilterForm(user_id=request.user)
        
    return render(request, 'demo/view_expenses.html', {'form': form,
        'latest_poll_list': latest_poll_list, 'expenses_sum': expenses_sum, })
def viewIncome(request):
    # if this is a POST request we need to process the form data
    latest_poll_list = Income.objects.filter(user__in=User.objects.filter(id=request.user.id))
    expenses_sum = latest_poll_list.aggregate(Sum('amount'))
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = IncomeFilterForm(request.POST, user_id=request.user)
        # check whether it's valid:
        if form.is_valid():
            name = request.POST['name']
            date_from = request.POST['date_from']
            date_to = request.POST['date_to']
            user = request.POST['user']
            account = request.POST['account']
            contractor = request.POST['contractor']
            if name:
                latest_poll_list = latest_poll_list.filter(name__contains=name)
            if int(user) != 0:
                latest_poll_list = latest_poll_list.filter(user=User.objects.get(id=user))
            if int(account) != 0:
                print(Accounts.objects.get(id=account).name)
                latest_poll_list = latest_poll_list.filter(account=Accounts.objects.get(id=account))
                print(latest_poll_list)
            if int(contractor) != 0:
                latest_poll_list = latest_poll_list.filter(contractor=contractor)
            if date_from:
                latest_poll_list = latest_poll_list.filter(date__gt=date_from)
            if date_to:
                latest_poll_list = latest_poll_list.filter(date__lt=date_to)    
            expenses_sum = latest_poll_list.aggregate(Sum('amount'))
            return render(request, 'demo/view_expenses.html', {'form': form,
        'latest_poll_list': latest_poll_list, 'expenses_sum': expenses_sum, })

    # if a GET (or any other method) we'll create a blank form
    else:
        form = IncomeFilterForm(user_id=request.user)
        
    return render(request, 'demo/view_income.html', {'form': form,
        'latest_poll_list': latest_poll_list, 'expenses_sum': expenses_sum, })
def viewAccounts(request):
    # if this is a POST request we need to process the form data
    latest_poll_list = Accounts.objects.filter(members__in=User.objects.filter(id=request.user.id))
    expenses_sum = latest_poll_list.aggregate(Sum('amount'))
    return render(request, 'demo/view_accounts.html', {'latest_poll_list': latest_poll_list, 'expenses_sum': expenses_sum, })

def editExpense(request):
    
    if request.method == 'POST':
        if 'tempId' in request.POST:
            id = request.POST['tempId']
            print(id)
            form = EditExpenseForm(expense=id, user_id=request.user)
        if 'name' in request.POST:
            id = request.POST['id']
            name = request.POST['name']
            date = request.POST['date']
            amount = request.POST['amount']
            accountNumber = request.POST['account']
            contractor = request.POST['contractor']
            fixed = False
            expense = Expenses.objects.get(id=id)
            if 'fixed' in request.POST:
                fixed = request.POST['fixed']
                expense.fixed = fixed
            
            expense.name = name
            expense.date = date
            a = Accounts.objects.get(id=accountNumber)
            a.amount = a.amount + float(expense.amount)
            expense.amount = amount
            expense.contractor = Contractors.objects.get(id=contractor)
            a.save()
            if 'toDelete' in request.POST:
                Expenses.objects.filter(id=id).delete()
                return HttpResponseRedirect("/home/")
            a.amount = a.amount - float(amount)
            a.save()
            expense.account = Accounts.objects.get(id=accountNumber)
            expense.save()
            u = Expenses.objects.filter()
            if 'subcategory' in request.POST:
                subcategory = request.POST['subcategory']
                expense.subcategory = Subcategory.objects.get(id=subcategory)
                expense.save()
            return HttpResponseRedirect("/home/")
        return render(request, 'demo/editExpenses.html', {'form': form, })    
    return render(request, 'demo/editExpenses.html', {})

def editIncome(request):
    
    if request.method == 'POST':
        if 'tempId' in request.POST:
            id = request.POST['tempId']
            form = EditIncomeForm(income=id, user_id=request.user)
        if 'name' in request.POST:
            id = request.POST['id']
            name = request.POST['name']
            date = request.POST['date']
            amount = request.POST['amount']
            accountNumber = request.POST['account']
            income = Income.objects.get(id=id)
            
            income.name = name
            income.date = date
            a = Accounts.objects.get(id=accountNumber)
            a.amount = a.amount - float(income.amount)
            income.amount = amount
            a.save()
            if 'toDelete' in request.POST:
                Expenses.objects.filter(id=id).delete()
                return HttpResponseRedirect("/home/")
            a.amount = a.amount + float(amount)
            a.save()
            income.account = Accounts.objects.get(id=accountNumber)
            income.save()
            u = Expenses.objects.filter()

            return HttpResponseRedirect("/home/")
        return render(request, 'demo/editIncome.html', {'form': form, })    
    return render(request, 'demo/editIncome.html', {})

def editAccount(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # check whether it's valid:
        if 'tempId' in request.POST:
             id = request.POST['tempId']
             id = id[:-1]
             print('moje id' + id)
             form = EditAccountForm(account=id, user_id=request.user)
        if 'name' in request.POST:
            name = request.POST['name']
            bankName = request.POST['bank_Name']
            comment = request.POST['comment']
            accountNumber = 0
            if 'account_Number' in request.POST:
                if request.POST['account_Number'] > 0:
                    accountNumber = request.POST['account_Number']
            accountState = request.POST['account_State']
            id = request.POST['id']
            acc = Accounts.objects.get(id=id)
            acc.name = name 
            acc.bankName = bankName 
            acc.comment = comment 
            acc.number = accountNumber 
            acc.amount = accountState
            acc.save()
            flush_transaction()
            return HttpResponseRedirect('/home/')
        return render(request, 'demo/editAccount.html', {'form': form})
    return render(request, 'demo/editAccount.html', {'form': form})

@transaction.commit_manually
def flush_transaction():
    transaction.commit()
    

# Create your views here.
