# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bootstrap3.exceptions import BootstrapError
from bootstrap3.utils import add_css_class
from bootstrap3.text import text_value, text_concat
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User
from django.template import Template, Context
from django.utils.unittest import TestCase

from expenses.models import Accounts


class EditAccountForm(forms.Form):
    """
    Form with a variety of widgets to test bootstrap3 rendering.
    """
    id = forms.CharField()
    name = forms.CharField(label='Nazwa*',required=True)
    bank_Name = forms.CharField(label='Nazwa banku',required=False)
    comment = forms.CharField(label='Komentarz',required=False)
    account_Number = forms.IntegerField(label='Numer konta',required=False, initial=0)
    account_State = forms.FloatField(label='Stan konta*',required=True)



    required_css_class = 'bootstrap3-req'
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        account = kwargs.pop('account')
        super(EditAccountForm, self).__init__(*args, **kwargs)
        print(account)
        self.fields['id'] = forms.CharField(initial=Accounts.objects.get(id=account).id)
        self.fields['id'].widget.attrs['readonly'] = True
        self.fields['id'].widget = forms.HiddenInput()
        self.fields['name'] = forms.CharField(required=True, initial=Accounts.objects.get(id=account).name)
        self.fields['bank_Name'] = forms.CharField(required=False, initial=Accounts.objects.get(id=account).bankName)
        self.fields['comment'] = forms.CharField(required=False, initial=Accounts.objects.get(id=account).comment)
        self.fields['account_Number'] = forms.IntegerField(initial=Accounts.objects.get(id=account).number)
        self.fields['account_State'] = forms.FloatField(required=True, initial=Accounts.objects.get(id=account).amount)
    def clean(self):

        cleaned_data = super(EditAccountForm, self).clean()
        # raise forms.ValidationError("Mój błąd")
        return cleaned_data


class TestFormWithoutRequiredClass(EditAccountForm):
    required_css_class = ''


def render_template(text, **context_args):
    """
    Create a template ``text`` that first loads bootstrap3.
    """
    template = Template("{% load bootstrap3 %}" + text)
    if not 'form' in context_args:
        context_args['form'] = EditAccountForm()
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



