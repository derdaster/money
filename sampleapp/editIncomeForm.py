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

from expenses.models import Accounts, Contractors, Subcategory, Category, Income


class EditIncomeForm(forms.Form):
    """
    Form with a variety of widgets to test bootstrap3 rendering.
    """
    id = forms.CharField()
    name = forms.CharField(label='Nazwa*',required=True)
    date = forms.DateField(label='Data*',required=True,widget = AdminDateWidget,initial = datetime.now())
    amount = forms.FloatField(label='Kwota*',required=True)
    account=forms.ChoiceField([(obj.id, obj.name) for obj in Accounts.objects.filter()],label='Konto*', required=True)
    contractor=forms.ChoiceField([(obj.id, obj.name) for obj in Contractors.objects.filter()], label='Kontrahent',required=False)


    required_css_class = 'bootstrap3-req'
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        income = kwargs.pop('income')
        super(EditIncomeForm, self).__init__(*args, **kwargs)
        self.fields['id'] = forms.CharField(initial=Income.objects.get(id=income).id)
        self.fields['id'].widget.attrs['readonly'] = True
        self.fields['id'].widget = forms.HiddenInput()
        self.fields['name'] = forms.CharField(label='Nazwa*',required=True,initial=Income.objects.get(id=income).name)
        self.fields['date'] = forms.DateField(required=True,widget = AdminDateWidget,initial = Income.objects.get(id=income).date)
        self.fields['amount'] = forms.FloatField(label='Kwota*',required=True,initial=Income.objects.get(id=income).amount)
        self.fields['account'].choices=[[Income.objects.get(id=income).id, Income.objects.get(id=income).account.name]] + [(obj.id, obj.name) for obj in Accounts.objects.filter(members__in=User.objects.filter(id=user_id.id))]
        self.fields['contractor'].choices=[(obj.id, obj.name) for obj in Contractors.objects.filter()]
    def clean(self):

        cleaned_data = super(EditIncomeForm, self).clean()
        #raise forms.ValidationError("Mój błąd")
        return cleaned_data


class TestFormWithoutRequiredClass(EditIncomeForm):
    required_css_class = ''


def render_template(text, **context_args):
    """
    Create a template ``text`` that first loads bootstrap3.
    """
    template = Template("{% load bootstrap3 %}" + text)
    if not 'form' in context_args:
        context_args['form'] = EditIncomeForm()
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



