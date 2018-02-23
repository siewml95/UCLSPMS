from django import forms
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from crispy_forms.layout import  Submit, Layout, Div, Fieldset,HTML,MultiField,Button
from crispy_forms.helper import FormHelper
from django.core.urlresolvers import reverse
from django_select2.forms import HeavySelect2Widget,ModelSelect2TagWidget, Select2TagWidget
from crispy_forms.bootstrap import PrependedText
from django.utils.encoding import force_text
from django.forms.models import ModelChoiceIterator
from django.db.models import Q,Count
from django.forms.renderers import get_default_renderer
from django.utils.safestring import mark_safe
import datetime
from .models import Project,Keyword
from crispy_forms.layout import Field
Field.template = "field.html"
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
    def value_from_datadict(self, data, files, name):
                print("value_from_datadict")
                values = super(ModelSelect2TagWidgetCustom,self).value_from_datadict(data, files, name)

                return []
class KeywordWidget(forms.MultiWidget):
    def __init__(self,attrs=None):
        widgets = [
            forms.TextInput(),
            forms.TextInput()
        ]
        super(KeywordWidget,self).__init__(widgets,attrs=attrs)

    def decompress(self, value):
        print("value")
        if value:
            return value.split(' ')
        return [None, None]

class MyField(forms.CharField):

    def prepare_value(self, value):
            keywords = ""
            requirements = []
            print(value)
            if value:
                for item in value:
                     print(item)
                     keywords = ''.join([keywords,',' ,item.title])

                return keywords
            else:
               return value


class ProjectModelForm(forms.ModelForm):
    STATUS_CHOICES = (
                (1, 'Draft'),
                (2, 'Active'),
    )
    class Meta:
        model = Project
        fields = ['title','company','summary','keywords','deadline','image','status']

        #fields = ['title','company','summary','deadline','image','status']
    #keywords = MyField(widget=forms.TextInput,required=False)
    #keywords = MyField(required=False)
    #keywords =  forms.ChoiceField(widget=HeavySelect2Widget(data_url="/project/ajax"))
    keywords = forms.ModelMultipleChoiceField(widget=ModelSelect2TagWidgetCustom(
        queryset=Keyword.objects.active(),
        search_fields=['title__icontains'],
     ), queryset=Keyword.objects.none(), required=False)
    #print(keywords.__dict__)
    #$requirements = MyField(widget=forms.TextInput,required=False).set_attributes_from_name("keywords")
    deadline =  forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    #keywords = forms.CharField(required=False)
    checkbox = forms.BooleanField(required=False)


    def save(self,created_by=None):
        # save both forms
        project =  super(ProjectModelForm, self).save()
        project.created_by = created_by
        print(self.cleaned_data)
        if self.cleaned_data.get("checkbox"):
            project.image = None
        project.save()
        print("image")
        print(project.image)
        return project

    def clean_deadline(self):
        date = self.cleaned_data['deadline']
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date
    def __init__(self,*args,**kwargs):
        super(ProjectModelForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id_project_form"
        self.helper.form_method = "POST"
        self.helper.form_action = '.'
        self.helper.form_class = 'form-horizontal container form-file'
        self.helper.label_class ="col-sm-3 text-sm-right"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
             Field('title',css_class="form-control col-sm-8",label_class = 'hello'),
             Field('image',template="file.html"),
             Field('checkbox',template="empty.html"),
             Field('summary',help_text="bitch",rows="6", css_class='input-xlarge'),
             Field('keywords',help_text="",data_tags="true",data_token_separators="[',']",data_minimum_input_length="0",data_delay="300",multiple="multiple",ajax__cache="true"),
             HTML('<div class="form-group"><div class="control-label col-sm-3"></div><span class="form-text offset-sm-3" style="color:black; font-size:13px;padding-left:10px;" display:inline><span class="badge badge-grey">Grey</span> Approved keywords.<br/> <span class="badge badge-success">Green</span> Users-created keywords.<br/><span class="badge badge-primary">Blue</span> Keywords not created yet</span>'),
             HTML("<div class='form-group'><div class=' control-label col-sm-3 text-sm-right' style='font-size:13px;'><p>Recommended:</p></div><div class='recommended </div>'><span></span></div></div>"),
             Field('company',css_class="form-control col-sm-8",label_class = 'hello'),
             Field('deadline'),
             Field('status'),
             Submit('submit','Submit',data_style="expand-right",css_class="ladda-button pull-right btn-primary")
        )
        #print(self.helper)

class ProjectModelUpdateForm(ProjectModelForm):
    STATUS_CHOICES = (
                (1, 'Draft'),
                (2, 'Active'),
                (3, 'Taken'),
                (4, 'Completed'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES)

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

class ProjectDetailFilterForm(forms.Form):

        title = forms.CharField(required=False)
        company = forms.CharField(required=False)
        summary = forms.ChoiceField(widget=Select2TagWidgetCustom,required=False)
        keywords = forms.ModelMultipleChoiceField(widget=ModelSelect2TagWidgetCustom(
                placeholder="Search for Keywords",
                queryset=Keyword.objects.active(),
                search_fields=['title__icontains'],
            ), queryset=Keyword.objects.active(), required=False)

            #$requirements = MyField(widget=forms.TextInput,required=False).set_attributes_from_name("keywords")
        deadline =  forms.DateField(required=False,
                widget=forms.TextInput(
                    attrs={'type': 'date'}
                )
            )
        STATUS_CHOICES = (
            (2, 'Active'),
            (3, 'Taken'),
            (4, 'Completed'),
            (5, 'Deadline Passed')
        )

        status = forms.MultipleChoiceField(choices=STATUS_CHOICES, widget=forms.CheckboxSelectMultiple)

        def __init__(self,*args,**kwargs):
            super(ProjectDetailFilterForm,self).__init__(*args,**kwargs)
            self.helper = FormHelper(self)
            self.helper.form_id = "id-personal"
            self.helper.form_method = "GET"
            self.helper.form_action = '/project'
            self.helper.form_class = 'form-horizontal filter'
            self.helper.field_class = "col-sm-12"
            self.helper.layout = Layout(
                 Div(
                   Div(
                      Field('title',placeholder="Type in title..."),
                      template = 'project/panel-content.html',
                      css_id="1",
                      css_class="Title"
                   ),
                   Div(
                      Field('company',placeholder="Type in Company..."),
                      template = 'project/panel-content.html',
                      title="Company",
                      css_id="2",
                      css_class="Company"
                   ),
                   Div(
                     Field('summary',template = 'project/filter-conditions.html',data_token_separators="[',']",data_minimum_results_for_search="-1",data_minimum_input_length="0",data_delay="300",multiple="multiple",ajax__cache="true"),
                     template = 'project/panel-content.html',
                     css_id="3",
                     css_class="Summary"
                  ),
                   Div(
                     Field('keywords',data_tags="false",template = 'project/filter-conditions.html',data_token_separators="[',']",data_minimum_results_for_search="-1",data_minimum_input_length="0",data_delay="300",multiple="multiple",ajax__cache="true"),
                     HTML('<span class="help-block" style="color:black" display:inline><span class="badge badge-grey">Grey</span> Approved keywords. <br /><span class="badge badge-success">Green</span> Users-created keywords. <br /><span class="badge badge-primary">Green</span> Keywords not created yet</span>'),
                     template = 'project/panel-content.html',
                     css_id="4",
                     css_class="Keywords"
                   ),
                   Div(
                     Field('deadline'),
                     template = 'project/panel-content.html',
                     css_id="5",
                     css_class="Deadline"
                   ),
                   Div(
                     Field('status'),
                     template = 'project/panel-content.html',
                     css_id="5",
                     css_class="Status"
                   ),
                    template = 'project/panel.html'
                 ),

                Submit('submit', 'Submit'),
                Button('reset', 'Reset'),

            )


class ProjectFilterForm(FormHelper):

        STATUS_CHOICES = (
                (2, 'Active'),
                (3, 'Taken'),
                (4, 'Completed'),
                (5, 'Deadline Passed')
            )

        form_id = "id-personal"
        form_method = "GET"
        form_action = '/project'
        form_class = 'form-horizontal filter'
        field_class = "col-sm-12"
        layout = Layout(
             Div(
               Div(
                  Field('title',placeholder="Type in title..."),
                  template = 'project/panel-content.html',
                  css_id="1",
                  css_class="Title",
               ),
               Div(
                  Field('company',placeholder="Type in Company..."),
                  template = 'project/panel-content.html',
                  title="Company",
                  css_id="2",
                  css_class="Company"
               ),
               Div(
                 Field('summary',template = 'project/filter-conditions.html',data_token_separators="[',']",data_minimum_results_for_search="-1",data_minimum_input_length="0",data_delay="300",multiple="multiple",ajax__cache="true"),
                 template = 'project/panel-content.html',
                 css_id="3",
                 css_class="Summary"
              ),
               Div(
                 Field('keywords',placeholder="Search for keywords",data_tags="false",template = 'project/filter-conditions.html',data_token_separators="[',']",data_minimum_results_for_search="-1",data_minimum_input_length="0",data_delay="300",multiple="multiple",ajax__cache="true"),
                     HTML('<span class="help-block" style="color:black" display:inline><span class="badge badge-grey">Grey</span> Approved keywords. <br /><span class="badge badge-success">Green</span> Users-created keywords. <br /><span class="badge badge-primary">Green</span> Keywords not created yet</span>'),
                 template = 'project/panel-content.html',
                 css_id="4",
                 css_class="Keywords"
               ),
               Div(
                  Field('deadline',placeholder="Type in Deadline"),
                 template = 'project/panel-content.html',
                 css_id="5",
                 css_class="Deadline"
               ),
               Div(
                     Field('status'),
                     template = 'project/panel-content.html',
                     css_id="6",
                     css_class="Status"
                   ),
                template = 'project/panel.html'


             ),

            Submit('submit', 'Submit'),
            Button('reset', 'Reset'),

        )
