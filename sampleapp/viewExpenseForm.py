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

from expenses.models import Accounts, Contractors, Subcategory, Budget, Category

MY_CHOICES = (
    ('1', ''),
    ('2', 'Tak'),
    ('3', 'Nie'),
)
def get_my_choices():
    # you place some logic here
    return MY_CHOICES
class ExpenseFilterForm(forms.Form):
    """
    Form with a variety of widgets to test bootstrap3 rendering.
    """

    name = forms.CharField(required=False)
    date_from = forms.DateField(widget=AdminDateWidget, initial=datetime.now(), required=False)
    date_to = forms.DateField(widget=AdminDateWidget, initial=datetime.now(), required=False)
    user = forms.ChoiceField([(obj.id, obj.username) for obj in User.objects.filter()])
    account = forms.ChoiceField([(obj.id, obj.name) for obj in Accounts.objects.filter()])
    contractor = forms.ChoiceField([(obj.id, obj.name) for obj in Contractors.objects.filter()], required=False)
    category = forms.ChoiceField([(obj.id, obj.name) for obj in Category.objects.filter()], required=False)
    closed=forms.ChoiceField(choices=MY_CHOICES)


    required_css_class = 'bootstrap3-req'
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super(ExpenseFilterForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(required=False)
        self.fields['date_from'] = forms.DateField(widget=AdminDateWidget, initial=datetime.now(), required=False)
        self.fields['date_to'] = forms.DateField(widget=AdminDateWidget, initial=datetime.now(), required=False)
        self.fields['user'].choices = [[0, 'Użytkownik']] + ([(obj.id, obj.username) for obj in User.objects.filter(id__in=Budget.objects.filter(id__in=Budget.objects.filter(members=User.objects.get(id=user_id.id))).values('members'))])
        self.fields['account'].choices = [[0, 'Konto']] + [(obj.id, obj.name+": "+"{:.2f}".format(obj.amount)+" zł" ) for obj in Accounts.objects.filter(members__in=User.objects.filter(id=user_id.id))]
        self.fields['contractor'].choices = [[0, 'Kontrahent']] + [(obj.id, obj.name) for obj in Contractors.objects.filter(budget__isnull=True)]+ [(obj.id, obj.name) for obj in Contractors.objects.filter(budget__in=Budget.objects.filter(members=user_id))]
        self.fields['category'].choices = [[0, 'Kategoria']] + [(obj.id, obj.name) for obj in Category.objects.filter(budget__isnull=True)]+ [(obj.id, obj.name) for obj in Category.objects.filter(budget__in=Budget.objects.filter(members=user_id))]
        self.fields['my_choice_field'] = forms.ChoiceField(
            choices=get_my_choices() )
    def clean(self):

        cleaned_data = super(ExpenseFilterForm, self).clean()
        # raise forms.ValidationError("Mój błąd")
        return cleaned_data


class TestFormWithoutRequiredClass(ExpenseFilterForm):
    required_css_class = ''


def render_template(text, **context_args):
    """
    Create a template ``text`` that first loads bootstrap3.
    """
    template = Template("{% load bootstrap3 %}" + text)
    if not 'form' in context_args:
        context_args['form'] = ExpenseFilterForm()
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



