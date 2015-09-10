# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from bootstrap3.exceptions import BootstrapError
from bootstrap3.utils import add_css_class
from bootstrap3.text import text_value, text_concat
from django import forms
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget 
from django.contrib.auth.models import User
from django.template import Template, Context
from django.utils.unittest import TestCase

from expenses.models import Accounts, Contractors, Subcategory, Category, \
    Expenses, Budget


class EditExpenseForm(forms.Form):
    """
    Form with a variety of widgets to test bootstrap3 rendering.
    """
#     date = forms.DateField(required=False)
#     subject = forms.CharField(
#         max_length=100,
#         help_text='my_help_text',
#         required=True,
#         widget=forms.TextInput(attrs={'placeholder': 'placeholdertest'}),
#     )
    id = forms.CharField()
    name = forms.CharField(label='Nazwa*',required=True)
    date = forms.DateField(label='Data*',required=True, widget=AdminDateWidget, initial=datetime.now())
    amount = forms.FloatField(label='Kwota*',required=True)
    account = forms.ChoiceField([(obj.id, obj.name) for obj in Accounts.objects.filter()],label='Konto*', required=True)
    contractor = forms.ChoiceField([(obj.id, obj.name) for obj in Contractors.objects.filter()], label='Kontrahent',required=False)
    subcategory = forms.ChoiceField([(obj.id, obj.name) for obj in Subcategory.objects.filter()], label='Podkategoria',required=False)
    fixed = forms.BooleanField(required=False,label='Stały wydatek',)
    to_Delete = forms.BooleanField(required=False,label='Do usunięcia',)


    required_css_class = 'bootstrap3-req'
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        expense = kwargs.pop('expense')
        super(EditExpenseForm, self).__init__(*args, **kwargs)
        print(expense)
        self.fields['id'] = forms.CharField(initial=Expenses.objects.get(id=expense).id)
        self.fields['id'].widget.attrs['readonly'] = True
        self.fields['id'].widget = forms.HiddenInput()
        self.fields['name'] = forms.CharField(required=True,initial=Expenses.objects.get(id=expense).name)
        self.fields['amount'] = forms.FloatField(required=True, initial=Expenses.objects.get(id=expense).amount)
        self.fields['date'] = forms.DateField(required=True, widget=AdminDateWidget, initial=Expenses.objects.get(id=expense).date)
        self.fields['account'].choices = [[Expenses.objects.get(id=expense).account.id, Expenses.objects.get(id=expense).account.name]] + [(obj.id, obj.name) for obj in Accounts.objects.filter(members__in=User.objects.filter(id=user_id.id))]
        self.fields['contractor'].choices = [(obj.id, obj.name) for obj in Contractors.objects.filter(budget__isnull=True)]+ [(obj.id, obj.name) for obj in Contractors.objects.filter(budget__in=Budget.objects.filter(members=user_id))]
        self.fields['subcategory'].choices = [[Expenses.objects.get(id=expense).subcategory.id, Expenses.objects.get(id=expense).subcategory]] + [(obj.id, Category.objects.get(id__in=Subcategory.objects.filter(id=obj.id).values('category')).name + ": " + obj.name) for obj in Subcategory.objects.filter()]
    def clean(self):

        cleaned_data = super(EditExpenseForm, self).clean()
        # raise forms.ValidationError("Mój błąd")
        return cleaned_data


class TestFormWithoutRequiredClass(EditExpenseForm):
    required_css_class = ''


def render_template(text, **context_args):
    """
    Create a template ``text`` that first loads bootstrap3.
    """
    template = Template("{% load bootstrap3 %}" + text)
    if not 'form' in context_args:
        context_args['form'] = EditExpenseForm()
    return template.render(Context(context_args))


def render_formset(formset=None, **context_args):
    """
    Create a template that renders a formset
    """
    context_args['formset'] = formset
    return render_template('{% bootstrap_formset formset %}', **context_args)


def render_form(form=None, **context_args):
    """
    Create a template that renders a form
    """
    if form:
        context_args['form'] = form
    return render_template('{% bootstrap_form form %}', **context_args)


def render_form_field(field, **context_args):
    """
    Create a template that renders a field
    """
    form_field = 'form.%s' % field
    return render_template('{% bootstrap_field ' + form_field + ' %}', **context_args)


def render_field(field, **context_args):
    """
    Create a template that renders a field
    """
    context_args['field'] = field
    return render_template('{% bootstrap_field field %}', **context_args)



