# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bootstrap3.exceptions import BootstrapError
from bootstrap3.utils import add_css_class
from bootstrap3.text import text_value, text_concat
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.template import Template, Context
from django.utils.unittest import TestCase

from expenses.models import Accounts


class TestForm(forms.Form):
    """
    Form with a variety of widgets to test bootstrap3 rendering.
    """

    name = forms.CharField(label='Imię',required=False)
    surname = forms.CharField(label='Nazwisko',required=False)
    nickname = forms.CharField(label='Login*',required=True)
    email=forms.EmailField(label='Email*',required=True)
    password = forms.CharField(label='Hasło*',widget=forms.PasswordInput,required=True)
    repeat_password = forms.CharField(label='Powtórz hasło*',widget=forms.PasswordInput,required=True)

    

    required_css_class = 'bootstrap3-req'

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('nickname')
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        user=False
        user = User.objects.filter(username=username).exists()
        if user is True:
            raise forms.ValidationError(u'Użytkownik "%s" już istnieje.' % username)
        user = User.objects.filter(email=email).exists()
        if user is True:
            raise forms.ValidationError(u'Użytkownik o podanym mailu: "%s" już istnieje.' % email)
        if len(password) < 8:
            raise ValidationError('Za krótkie hasło-minimum 8 liter')
        if password!=repeat_password:
            raise ValidationError('Podane hasła są różne')
        cleaned_data = super(TestForm, self).clean()
        #raise forms.ValidationError("Mój błąd")
        return cleaned_data


class TestFormWithoutRequiredClass(TestForm):
    required_css_class = ''


def render_template(text, **context_args):
    """
    Create a template ``text`` that first loads bootstrap3.
    """
    template = Template("{% load bootstrap3 %}" + text)
    if not 'form' in context_args:
        context_args['form'] = TestForm()
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



