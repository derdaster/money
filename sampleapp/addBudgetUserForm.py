# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bootstrap3.exceptions import BootstrapError
from bootstrap3.utils import add_css_class
from bootstrap3.tests import TestForm
from bootstrap3.text import text_value, text_concat
from django import forms
from django.contrib.auth.models import User
from django.db.models.constants import LOOKUP_SEP
from django.template import Template, Context
from django.utils.unittest import TestCase

from expenses.models import Accounts, Budget


class BudgetUserForm(forms.Form):
    """
    Form with a variety of widgets to test bootstrap3 rendering.
    """
    budget=forms.ChoiceField(label='Budżet')
    name = forms.CharField(label='Nazwa*',required=True)
    


    required_css_class = 'bootstrap3-req'

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')

        super(BudgetUserForm, self).__init__(*args, **kwargs)
        self.fields['budget'].choices=[(obj.id, obj.name) for obj in Budget.objects.filter(members=User.objects.get(id=user_id.id))]
    
        
    def clean(self):
        name = self.cleaned_data.get('name')
        name2 = User.objects.filter(username=name).exists()
        if name2 is False:
            raise forms.ValidationError(u'Użytkownik "%s"nie istnieje.' % name)
        cleaned_data = super(BudgetUserForm, self).clean()
        # raise forms.ValidationError("Mój błąd")
        return cleaned_data


class TestFormWithoutRequiredClass(BudgetUserForm):
    required_css_class = ''


def render_template(text, **context_args):
    """
    Create a template ``text`` that first loads bootstrap3.
    """
    template = Template("{% load bootstrap3 %}" + text)
    if not 'form' in context_args:
        context_args['form'] = BudgetUserForm()
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

class SettingsTest(TestCase):        

    def test_settings_filter(self):
        res = render_template('{% load bootstrap3 %}{{ "required_css_class"|bootstrap_setting }}')
        self.assertEqual(res.strip(), 'bootstrap3-req')
        res = render_template(
            '{% load bootstrap3 %}{% if "javascript_in_head"|bootstrap_setting %}head{% else %}body{% endif %}')
        self.assertEqual(res.strip(), 'head')

    def test_required_class(self):
        form = BudgetUserForm()
        res = render_template('{% bootstrap_form form %}', form=form)
        self.assertIn('bootstrap3-req', res)

    def test_error_class(self):
        form = BudgetUserForm({})
        res = render_template('{% bootstrap_form form %}', form=form)
        self.assertIn('bootstrap3-err', res)

    def test_bound_class(self):
        form = BudgetUserForm({'sender': 'sender'})
        res = render_template('{% bootstrap_form form %}', form=form)
        self.assertIn('bootstrap3-bound', res)


class TemplateTest(TestCase):
    def test_empty_template(self):
        res = render_template('')
        self.assertEqual(res.strip(), '')

    def test_text_template(self):
        res = render_template('some text')
        self.assertEqual(res.strip(), 'some text')

    def test_bootstrap_template(self):
        template = Template((
            '{% extends "bootstrap3/bootstrap3.html" %}{% block bootstrap3_content %}test_bootstrap3_content{% endblock %}'))
        res = template.render(Context({}))
        self.assertIn('test_bootstrap3_content', res)

    def test_javascript_without_jquery(self):
        res = render_template('{% bootstrap_javascript jquery=0 %}')
        self.assertIn('bootstrap', res)
        self.assertNotIn('jquery', res)

    def test_javascript_with_jquery(self):
        res = render_template('{% bootstrap_javascript jquery=1 %}')
        self.assertIn('bootstrap', res)
        self.assertIn('jquery', res)


class FormSetTest(TestCase):
    def test_illegal_formset(self):
        with self.assertRaises(BootstrapError):
            render_formset(formset='illegal')


class FormTest(TestCase):
    def test_illegal_form(self):
        with self.assertRaises(BootstrapError):
            render_form(form='illegal')

    def test_field_names(self):
        form = BudgetUserForm()
        res = render_form(form)
        for field in form:
            self.assertIn('name="%s"' % field.name, res)

    def test_exclude(self):
        form = BudgetUserForm()
        res = render_template('{% bootstrap_form form exclude="cc_myself" %}', form=form)
        self.assertNotIn('cc_myself', res)

    def test_layout_horizontal(self):
        form = BudgetUserForm()
        res = render_template('{% bootstrap_form form layout="horizontal" %}', form=form)
        self.assertIn('col-md-2', res)
        self.assertIn('col-md-4', res)
        res = render_template('{% bootstrap_form form layout="horizontal" horizontal_label_class="hlabel" horizontal_field_class="hfield" %}', form=form)
        self.assertIn('hlabel', res)
        self.assertIn('hfield', res)

    def test_buttons_tag(self):
        form = BudgetUserForm()
        res = render_template('{% buttons layout="horizontal" %}{% endbuttons %}', form=form)
        self.assertIn('col-md-2', res)
        self.assertIn('col-md-4', res)


class FieldTest(TestCase):
    def test_illegal_field(self):
        with self.assertRaises(BootstrapError):
            render_field(field='illegal')

    def test_show_help(self):
        res = render_form_field('subject')
        self.assertIn('my_help_text', res)
        self.assertNotIn('<i>my_help_text</i>', res)
        res = render_template('{% bootstrap_field form.subject show_help=0 %}')
        self.assertNotIn('my_help_text', res)

    def test_subject(self):
        res = render_form_field('subject')
        self.assertIn('type="text"', res)
        self.assertIn('placeholder="placeholdertest"', res)

    def test_required_field(self):
        required_field = render_form_field('subject')
        self.assertIn('required', required_field)
        self.assertIn('bootstrap3-req', required_field)
        not_required_field = render_form_field('message')
        self.assertNotIn('required', not_required_field)
        # Required field with required=0
        form_field = 'form.subject'
        rendered = render_template('{% bootstrap_field ' + form_field + ' set_required=0 %}')
        self.assertNotIn('required', rendered)
        # Required settings in field
        form_field = 'form.subject'
        rendered = render_template('{% bootstrap_field ' + form_field + ' required_css_class="test-required" %}')
        self.assertIn('test-required', rendered)

    def test_empty_permitted(self):
        form = BudgetUserForm()
        res = render_form_field('subject', form=form)
        self.assertIn('required', res)
        form.empty_permitted = True
        res = render_form_field('subject', form=form)
        self.assertNotIn('required', res)


    def test_input_group(self):
        res = render_template('{% bootstrap_field form.subject addon_before="$" addon_after=".00" %}')
        self.assertIn('class="input-group"', res)
        self.assertIn('class="input-group-addon">$', res)
        self.assertIn('class="input-group-addon">.00', res)

    def test_size(self):
        def _test_size(param, klass):
            res = render_template('{% bootstrap_field form.subject size="' + param + '" %}')
            self.assertIn(klass, res)
        def _test_size_medium(param):
            res = render_template('{% bootstrap_field form.subject size="' + param + '" %}')
            self.assertNotIn('input-lg', res)
            self.assertNotIn('input-sm', res)
            self.assertNotIn('input-md', res)
        _test_size('sm', 'input-sm')
        _test_size('small', 'input-sm')
        _test_size('lg', 'input-lg')
        _test_size('large', 'input-lg')
        _test_size_medium('md')
        _test_size_medium('medium')
        _test_size_medium('')


class ComponentsTest(TestCase):
    def test_icon(self):
        res = render_template('{% bootstrap_icon "star" %}')
        self.assertEqual(res.strip(), '<span class="glyphicon glyphicon-star"></span>')
        res = render_template('{% bootstrap_icon "star" title="alpha centauri" %}')
        self.assertEqual(res.strip(), '<span class="glyphicon glyphicon-star" title="alpha centauri"></span>')

    def test_alert(self):
        res = render_template('{% bootstrap_alert "content" alert_type="danger" %}')
        self.assertEqual(res.strip(), '<div class="alert alert-danger alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>content</div>')


class MessagesTest(TestCase):
    def test_messages(self):
        class FakeMessage(object):
            """
            Follows the `django.contrib.messages.storage.base.Message` API.
            """

            def __init__(self, message, tags):
                self.tags = tags
                self.message = message

            def __str__(self):
                return self.message

        messages = [FakeMessage("hello", "warning")]
        res = render_template('{% bootstrap_messages messages %}', messages=messages)
        expected = """
    <div class="alert alert-warning alert-dismissable">
        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&#215;</button>
        hello
    </div>
"""
        self.assertEqual(res.strip(), expected.strip())

        messages = [FakeMessage("hello", "error")]
        res = render_template('{% bootstrap_messages messages %}', messages=messages)
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&#215;</button>
        hello
    </div>
        """
        self.assertEqual(res.strip(), expected.strip())

        messages = [FakeMessage("hello", None)]
        res = render_template('{% bootstrap_messages messages %}', messages=messages)
        expected = """
    <div class="alert alert-dismissable">
        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&#215;</button>
        hello
    </div>
"""
        self.assertEqual(res.strip(), expected.strip())


class TextTest(TestCase):
    def test_add_css_class(self):
        css_classes = "one two"
        css_class = "three four"
        classes = add_css_class(css_classes, css_class)
        self.assertEqual(classes, "one two three four")

        classes = add_css_class(css_classes, css_class, prepend=True)
        self.assertEqual(classes, "three four one two")


class HtmlTest(TestCase):
    def test_text_value(self):
        self.assertEqual(text_value(''), "")
        self.assertEqual(text_value(' '), " ")
        self.assertEqual(text_value(None), "")
        self.assertEqual(text_value(1), "1")

    def test_text_concat(self):
        self.assertEqual(text_concat(1, 2), "12")
        self.assertEqual(text_concat(1, 2, separator='='), "1=2")
        self.assertEqual(text_concat(None, 2, separator='='), "2")


class ButtonTest(TestCase):
    def test_button(self):
        res = render_template("{% bootstrap_button 'button' size='lg' %}")
        self.assertEqual(res.strip(), '<button class="btn btn-lg">button</button>')
        res = render_template("{% bootstrap_button 'button' size='lg' href='#' %}")
        self.assertIn(res.strip(), '<a class="btn btn-lg" href="#">button</a><a href="#" class="btn btn-lg">button</a>')

