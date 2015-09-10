# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bootstrap3.exceptions import BootstrapError
from bootstrap3.utils import add_css_class
from bootstrap3.text import text_value, text_concat
from django import forms
from django.template import Template, Context
from django.utils.unittest import TestCase

from expenses.models import Category, Budget, Subcategory


class SubcategoryForm(forms.Form):
    """
    Form with a variety of widgets to test bootstrap3 rendering.
    """
    category=forms.ChoiceField(label='Kategoria',required=True)
    name = forms.CharField(label='Nazwa*',required=True)
    required_css_class = 'bootstrap3-req'
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super(SubcategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices=[(obj.id, obj.name) for obj in Category.objects.filter(budget__isnull=True)]+ [(obj.id, obj.name) for obj in Category.objects.filter(budget__in=Budget.objects.filter(members=user_id))]
    def clean(self):
        category = self.cleaned_data.get('category')
        subname = self.cleaned_data.get('name')
        category2 = Category.objects.get(id=category)
        subcategory = Subcategory.objects.filter(name=subname,category=category2).exists()
        if subcategory is True:
            raise forms.ValidationError(u'Podkategoria "%s" już istnieje.' % subname)
        cleaned_data = super(SubcategoryForm, self).clean()
        #raise forms.ValidationError("Mój błąd")
        return cleaned_data


class TestFormWithoutRequiredClass(SubcategoryForm):
    required_css_class = ''


def render_template(text, **context_args):
    """
    Create a template ``text`` that first loads bootstrap3.
    """
    template = Template("{% load bootstrap3 %}" + text)
    if not 'form' in context_args:
        context_args['form'] = SubcategoryForm()
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



