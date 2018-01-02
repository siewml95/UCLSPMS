from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User,Interest,Profile
from project.models import Keyword
from project.forms import ModelSelect2TagWidgetCustom
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from crispy_forms.layout import  Submit, Layout, Div, Fieldset,HTML,MultiField
from django_select2.forms import HeavySelect2Widget,ModelSelect2TagWidget

class CustomUserStaffCreationForm(UserCreationForm):
    """ A form for creating new users. Includes all the required fields, plus a repeated password. """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
    email = forms.CharField(max_length=75, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        #Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        #Save the provided password in hashed format
        user = super(CustomUserStaffCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        print("save")
        user.type = 3
        print(user.type)
        if commit:
            user.save()
        print(user.__dict__)
        return user



    def __init__(self,*args,**kwargs):
        super(CustomUserStaffCreationForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-personal"
        self.helper.form_method = "POST"
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit','Submit',data_style="expand-right",css_class="ladda-button btn-primary"))
        self.helper.form_class = 'form-horizontal container'
        self.helper.label_class ="col-sm-2"
        self.helper.field_class = "col-sm-10"
        self.helper.layout = Layout(
             Field('username',css_class="form-control col-sm-10",label_class = 'hello'),
             Field('email', rows="6", css_class='input-xlarge'),
             Field('password1', rows="6", css_class='input-xlarge'),
             Field('password2', rows="6", css_class='input-xlarge'),

        )

class CustomUserCreationForm(UserCreationForm):
    """ A form for creating new users. Includes all the required fields, plus a repeated password. """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
    email = forms.CharField(max_length=75, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        #Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        #Save the provided password in hashed format
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.type = 1
        if commit:
            user.save()
        print(user.__dict__)
        return user



    def __init__(self,*args,**kwargs):
        super(CustomUserCreationForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-personal"
        self.helper.form_method = "POST"
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit','Submit',data_style="expand-right",css_class="ladda-button btn-primary"))
        self.helper.form_class = 'form-horizontal container'
        self.helper.label_class ="col-sm-2"
        self.helper.field_class = "col-sm-10"
        self.helper.layout = Layout(
             Field('username',css_class="form-control col-sm-10",label_class = 'hello'),
             Field('email', rows="6", css_class='input-xlarge'),
             Field('password1', rows="6", css_class='input-xlarge'),
             Field('password2', rows="6", css_class='input-xlarge'),

        )

class UserForm(forms.ModelForm):

    class Meta:
     model = User
     fields = ('email', 'first_name', 'last_name')


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # magic
        print("UserProfileForm")
        print(kwargs['instance'])
        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.uf = UserForm(*args, **user_kwargs)
        # magic end

        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields.update(self.uf.fields)
        self.initial.update(self.uf.initial)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-personal"
        self.helper.form_method = "POST"

        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit','Submit',data_style="expand-right",css_class="ladda-button btn-primary"))
        self.helper.form_class = 'form-horizontal container'
        self.helper.label_class ="col-sm-2"
        self.helper.field_class = "col-sm-10"
        self.helper.layout = Layout(
             Field('email', rows="6", css_class='input-xlarge'),
             Field('first_name', rows="6", css_class='input-xlarge'),
             Field('last_name', rows="6", css_class='input-xlarge'),
             Field('avatar',template="user/profile/avatar.html",rows="6", css_class='input-xlarge')
        )
        # define fields order if needed


    def save(self,*args, **kwargs):
        # save both forms
        self.uf.save(*args, **kwargs)
        return super(UserProfileForm, self).save(*args, **kwargs)

    class Meta:
        model = Profile
        fields = ('avatar',)

class UserProfilePreferenceForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('preferences',)
    preferences = forms.ModelMultipleChoiceField(widget=ModelSelect2TagWidgetCustom(
        queryset=Keyword.objects.all(),
        search_fields=['title__icontains'],
    ), queryset=Keyword.objects.all(), required=False)
    def __init__(self,*args,**kwargs):
        super(UserProfilePreferenceForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-personal"
        self.helper.form_method = "POST"
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit','Submit',data_style="expand-right",css_class="ladda-button btn-primary"))
        self.helper.form_class = 'form-horizontal container'
        self.helper.label_class ="col-sm-2"
        self.helper.field_class = "col-sm-10"
        self.helper.layout = Layout(
             Field('preferences',data_tags="true",data_token_separators="[',']",data_minimum_input_length="0",data_delay="300",multiple="multiple",ajax__cache="true"),
             HTML('<div class="control-label col-sm-2"></div><span class="help-block" display:inline>Grey: approved keywords. Green : users created keywords. Blue : keywords not created yet</span>'),

        )
class UserProfilePasswordForm(forms.ModelForm):

    class Meta:
     model = User
     fields = ("last_login",)

    passwordcurrent = forms.CharField(label='Password Current', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)


    def clean_passwordcurrent(self,*args,**kwargs):
        passwordcurrent = self.cleaned_data.get("passwordcurrent")
        print("current_passwordcurrrent")
        print(self.request.user)
        if self.request is not None and self.request.user is not None:
           user = User.objects.get(pk=self.request.user.pk)
        else :
           user = User.objects.get(pk=self.initial["id"])
        if user.check_password(passwordcurrent):
            return passwordcurrent
        else:
            raise forms.ValidationError("Wrong password.")
    def clean_password2(self):
        #Check that the two password entries match
        print("clean password")
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        print("ok")
        return password2

    def save(self, commit=True):
        #Save the provided password in hashed format
        print("save")

        user = super(UserProfilePasswordForm, self).save(commit=False)
        print("save")
        print(self.cleaned_data.get("password1"))
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        print(user.__dict__)
        return user

    def __init__(self,*args,**kwargs):
        print("passwordForm")
        self.request = kwargs.pop('request')
        super(UserProfilePasswordForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-personal"
        self.helper.form_method = "POST"
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit','Submit',data_style="expand-right",css_class="ladda-button btn-primary"))
        self.helper.form_class = 'form-horizontal container'
        self.helper.label_class ="col-sm-2"
        self.helper.field_class = "col-sm-10"
        self.helper.layout = Layout(
             Field('passwordcurrent', rows="6", css_class='input-xlarge'),
             Field('password1', rows="6", css_class='input-xlarge'),
             Field('password2', rows="6", css_class='input-xlarge'),

        )

class InterestForm(forms.Form):
   description = forms.CharField(widget=forms.Textarea,required=False,label="Why are your interested in this project?")


class BugForm(forms.Form):
   content = forms.CharField(widget=forms.Textarea,required=True,label="Report Bugs")

class BugWithEmailForm(forms.Form):
   email = forms.EmailField(required=True,label="Email")
   content = forms.CharField(widget=forms.Textarea,required=True,label="Report Bugs")
