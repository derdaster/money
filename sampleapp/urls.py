from __future__ import unicode_literals

from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from sampleapp import settings
from sampleapp .views import FormHorizontalView, AddUserView, AddBudgetUserView, AddAccountView, AddExpenseView, AddAccuserView, AddBudgetView, AddContractorView, AddCategoryView, AddLoginView, AddLogoutView, LoggedView, \
    viewAccounts, editExpense, submitIncome, viewIncome, editAccount, editIncome

from .views import IndexView, submitForm, submitBudgetUser, submitAccount, submitExpense, submitAccuser, submitBudget, submitContractor, submitCategory, submitSubcategory, submitLogin, logOut, getExpenses, viewExpenses, closeExpenses
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^home/', login_required(LoggedView.as_view()), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^add_user', AddUserView.as_view(success_url="/success/"), name='add_user'),
    url(r'^add_budgetuser', login_required(submitBudgetUser), name='add_budgetuser'),
    url(r'^add_budget', login_required(AddBudgetView.as_view(success_url="/success2/")), name='add_budget'),
    url(r'^add_account', login_required(AddAccountView.as_view(success_url="/success2/")), name='add_account'),
    url(r'^add_expense', login_required(submitExpense), name='add_expense'),
    url(r'^add_income', login_required(submitIncome), name='add_income'),
    url(r'^add_accuser', login_required(submitAccuser), name='add_accuser'),
    url(r'^add_contractor', login_required(AddContractorView.as_view(success_url="/success2/")), name='add_contractor'),
    url(r'^add_category', login_required(AddCategoryView.as_view(success_url="/success2/")), name='add_category'),
    url(r'^add_subcategory', login_required(submitSubcategory), name='add_subcategory'),
    url(r'^add_login', AddLoginView.as_view(success_url="/success2/"), name='add_login'),
    url(r'^logout', login_required(AddLogoutView.as_view(success_url="/success2/")), name='logout'),
    url(r'^success/', login_required(LoggedView.as_view()), name='home'),
    url(r'^success2/', login_required(LoggedView.as_view()), name='home'),
    url(r'^submitForm/', submitForm),
    url(r'^submitBudget/', login_required(submitBudget)),
    url(r'^submitBudgetUser/', login_required(submitBudgetUser)),
    url(r'^submitAccount/', login_required(submitAccount)),
    url(r'^submitExpense/', login_required(submitExpense)),
    url(r'^submitContractor/', login_required(submitContractor)),
    url(r'^submitCategory/', login_required(submitCategory)),
    url(r'^submitSubcategory/', login_required(submitSubcategory)),
    url(r'^submitAccuser/', login_required(submitAccuser)),
    url(r'^submitLogin/', submitLogin),
    url(r'^logOut/', login_required(logOut),name='logOut'),
    url(r'^expenses/', login_required(getExpenses), name='expenses'),
    url(r'^expenseList/', login_required(viewExpenses), name='expensesList'),
    url(r'^incomeList/', login_required(viewIncome), name='incomeList'),
    url(r'^accountsList/', login_required(viewAccounts), name='accountsList'),
    url(r'^editExpense/', login_required(editExpense), name='editExpense'),
    url(r'^closeExpenses/', login_required(closeExpenses), name='closeExpenses'),
    url(r'^editIncome/', login_required(editIncome), name='editIncome'),
    url(r'^editAccount/', login_required(editAccount), name='editAccount'),
    url(r'^submitIncome/', login_required(submitIncome)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
 {'document_root': settings.STATIC_ROOT}),
)
