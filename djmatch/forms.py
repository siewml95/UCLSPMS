from django import forms
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from crispy_forms.layout import  Submit, Layout, Div, Fieldset,HTML,MultiField,Button
from crispy_forms.helper import FormHelper

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self,*args,**kwargs):
        super(ContactForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id_contact_form"
        self.helper.form_method = "POST"
        self.helper.form_action = '.'
        self.helper.form_class = 'form-horizontal container'
        self.helper.label_class ="col-sm-3 text-sm-right"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
             Field('name',css_class="form-control ",label_class = 'hello'),
             Field('email',css_class="form-control ",label_class = 'hello'),
             Field('message',css_class="form-control ",label_class = 'hello'),
             Submit('submit','Submit',data_style="expand-right",css_class="ladda-button pull-right btn-primary")
        )
