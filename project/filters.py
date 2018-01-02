import django_filters
import ast
from .models import Project,Keyword
from .forms import ProjectFilterForm
from itertools import chain
from collections import Counter
from django import forms
from django.db import models
from django.db.models import Q,Count
import operator
from  functools import reduce
from django.utils import timezone
from django_select2.forms import HeavySelect2Widget,ModelSelect2TagWidget,Select2TagWidget
from django.utils.encoding import force_text
from django.forms.models import ModelChoiceIterator
from django.db.models.query import QuerySet

class ChoiceFieldCustom(forms.ChoiceField):
    def validate(self, value):
        pass

    def valid_value(self, value):
        "Check to see if the provided value is a valid choice"
        return True

class ChoiceFilterCustom(django_filters.ChoiceFilter):
    field_class = ChoiceFieldCustom

class ModelSelect2TagWidgetCustom(ModelSelect2TagWidget):

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        print("create_option")
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)
        if 'type' in attrs:
            option_attrs['data-type'] = attrs['type']
        print(attrs)

        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
        }



    def optgroups(self, name, value, attrs=None):
        print("optgroups")
        """Return only selected options and set QuerySet from `ModelChoicesIterator`."""
        default = (None, [], 0)
        groups = [default]
        has_selected = False
        selected_choices = {force_text(v) for v in value}
        if not self.is_required and not self.allow_multiple_selected:
            default[1].append(self.create_option(name, '', '', False, 0))
        if not isinstance(self.choices, ModelChoiceIterator):
            return super(ModelSelect2TagWidgetCustom, self).optgroups(name, value, attrs=attrs)
        selected_choices = {
            c for c in selected_choices
            if c not in self.choices.field.empty_values
        }
        choices = (
            (obj.pk, self.label_from_instance(obj),obj.type)
            for obj in self.choices.queryset.filter(pk__in=selected_choices)
        )
        for option_value, option_label , option_type in choices:
            print(option_type)
            selected = (
                force_text(option_value) in value and
                (has_selected is False or self.allow_multiple_selected)
            )
            if selected is True and has_selected is False:
                has_selected = True
            index = len(default[1])
            subgroup = default[1]
            print(name)
            subgroup.append(self.create_option(name, option_value, option_label, selected_choices, index,attrs={"type":option_type}))
        print(groups)
        return groups

    def render_options(self, *args):
        print("render_options")
        """Render only selected options and set QuerySet from :class:`ModelChoiceIterator`."""
        try:
            selected_choices, = args
        except ValueError:
            choices, selected_choices = args
            choices = chain(self.choices, choices)
        else:
            choices = self.choices
        selected_choices = {force_text(v) for v in selected_choices}
        output = ['<option value=""></option>' if not self.is_required and not self.allow_multiple_selected else '']
        if isinstance(self.choices, ModelChoiceIterator):
            if self.queryset is None:
                self.queryset = self.choices.queryset
            selected_choices = {c for c in selected_choices
                                if c not in self.choices.field.empty_values}
            choices = [(obj.pk, self.label_from_instance(obj))
                       for obj in self.choices.queryset.filter(pk__in=selected_choices)]
        else:
            choices = [(k, v) for k, v in choices if force_text(k) in selected_choices]
        for option_value, option_label in choices:
            output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)

class Select2TagWidgetCustom(Select2TagWidget):
            def value_from_datadict(self, data, files, name):
                values = super(Select2TagWidgetCustom, self).value_from_datadict(data, files, name)
                if values is None:
                 return []
                else:
                 return values
            def optgroups(self, name, value, attrs=None):
                selected = set(value)
                subgroup = [self.create_option(name, v, v, selected, i) for i, v in enumerate(value)]
                return [(None, subgroup, 0)]


class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = ['deadline']


    title = django_filters.CharFilter(method="title_contains")
    company = django_filters.CharFilter(method="title_contains")
    strict = django_filters.BooleanFilter(label="Strict",method="nothing")
    summary = ChoiceFilterCustom(widget=Select2TagWidgetCustom,method="summary_filter")
    #keywords = django_filters.CharFilter(method="keywords_filter")
    #keywords = django_filters.CharFilter()
    #selectKeywords = django_filters.ChoiceFilter(method="keywords_filter")
    keywords = django_filters.ModelMultipleChoiceFilter(widget=ModelSelect2TagWidgetCustom(
            queryset=Keyword.objects.all(),
            search_fields=['title__icontains'],
        ), queryset=Keyword.objects.all(), error_messages={'invalid_pk_value':'hello'},required=False,method="keywords_filter")
    deadline = django_filters.DateFilter(label="Deadline Before",
        widget=forms.TextInput(
            attrs={'type': 'date'}
    ),method="deadline_filter")


    def title_contains(self,queryset,name,value):
        return queryset.filter(title__icontains=value)
    def nothing(self, queryset, name, value):
        return queryset
    def filter_contains(self, queryset, name, value):
        # construct the full lookup expression.
        lookup = '__'.join([name, 'icontains'])
        print(value)
        return queryset.filter(**{lookup: value})


    def summary_filter(self,queryset,name,value):
        if value is not None:
            value = ast.literal_eval(value)
        else:
            value = []
        if self.data and self.data.get("strict_id_summary") == "1":
         k_expressions = [Q(summary__icontains=val) for val in value]
         q = queryset.filter(reduce(operator.or_, k_expressions))
         return q
        else:
         q = queryset
         for k in value:
            q = q.filter(Q(summary__icontains=k))
         return q


    def deadline_filter(self,queryset,name,value):
        return queryset.filter(deadline__lte=value)

    def keywords_filter(self, queryset, name, value):
        print("keywords_filter")
        print(value)
        if self.data and self.data.get("strict_id_keywords") == "1":
            q = []
            q_expressions = [Q(keywords=keyword.id) for keyword in value]
            print(q_expressions)
            if q_expressions == [] :
               return q
            else :
                  q = queryset.filter(reduce(operator.or_, q_expressions))
                  print("strict")
                  print(q)
                  print(queryset.filter(reduce(operator.or_, q_expressions)).query)

                  k = q.values("slug","pk","title","summary").annotate(keyword_count=Count("keywords")).order_by('-keyword_count')
                  print("q")
                  print(k)
                  return k.order_by("-timestamp")
        else:
                q = queryset
                for k in value:
                        q = q.filter(keywords=k)
                return q.order_by("-timestamp")
