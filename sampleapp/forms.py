# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory

from sampleapp.addAccountForm import AccountForm
from sampleapp.addAccuserForm import AccuserForm
from sampleapp.addBudgetForm import BudgetForm
from sampleapp.addBudgetUserForm import BudgetUserForm
from sampleapp.addCategoryForm import CategoryForm
from sampleapp.addContractorForm import ContractorForm
from sampleapp.addExpenseForm import ExpenseForm
from sampleapp.addIncomeForm import IncomeForm
from sampleapp.addLoginForm import LoginForm
from sampleapp.addLogoutForm import LogoutForm
from sampleapp.addSubategoryForm import SubcategoryForm
from sampleapp.addUserForm import TestForm
from sampleapp.editAccountForm import EditAccountForm
from sampleapp.editExpenseForm import EditExpenseForm
from sampleapp.viewExpenseForm import ExpenseFilterForm
from sampleapp.viewIncomeForm import IncomeFilterForm
from sampleapp.editIncomeForm import EditIncomeForm

class ContactForm(TestForm):
    pass
class BudgetForm(BudgetForm):
    pass
class BudgetUser(BudgetUserForm):
    pass
class AccountForm(AccountForm):
    pass
class ExpenseForm(ExpenseForm):
    pass
class AccuserForm(AccuserForm):
    pass
class ContractorForm(ContractorForm):
    pass
class CategoryForm(CategoryForm):
    pass
class SubcategoryForm(SubcategoryForm):
    pass
class ExpenseFilterForm(ExpenseFilterForm):
    pass
class EditExpenseForm(EditExpenseForm):
    pass
class IncomeForm(IncomeForm):
    pass
class EditAccountForm(EditAccountForm):
    pass
class IncomeFilterForm(IncomeFilterForm):
    pass
class EditIncomeForm(EditIncomeForm):
    pass
class LoginForm(LoginForm):
    pass
class LogoutForm(LogoutForm):
    pass
class ContactBaseFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(ContactBaseFormSet, self).add_fields(form, index)

    def clean(self):
        super(ContactBaseFormSet, self).clean()
        raise forms.ValidationError("Wypełnij wszystike wymagane pola")

ContactFormSet = formset_factory(TestForm, formset=ContactBaseFormSet,
                                 extra=2,
                                 max_num=4,
                                 validate_max=True)


class FilesForm(forms.Form):
    text1 = forms.CharField()
    file1 = forms.FileField()
    file2 = forms.FileField(required=False)
    file3 = forms.FileField(widget=forms.ClearableFileInput)
    file4 = forms.FileField(required=False, widget=forms.ClearableFileInput)


class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()

    def clean(self):
        cleaned_data = super(ArticleForm, self).clean()
        raise forms.ValidationError("Wypełnij wszystike wymagane pola.")
        return cleaned_data
