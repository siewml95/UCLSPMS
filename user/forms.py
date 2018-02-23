from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Interest,Profile,Subscription
from project.models import Keyword
from project.forms import ModelSelect2TagWidgetCustom
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from crispy_forms.layout import  Submit, Layout, Div, Fieldset,HTML,MultiField
from django_select2.forms import HeavySelect2Widget,ModelSelect2TagWidget
import string,random,datetime
from django.contrib.auth import forms as authForms
from cuser.forms import AuthenticationForm as CUserAuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login, authenticate
from cuser.models import CUser as User
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.urls import reverse
from crispy_forms.layout import Field
Field.template = "field.html"

class CustomUserStaffCreationForm(UserCreationForm):
    error_messages = {
            'password_mismatch': _("The two password fields didn't match."),
        }
    """ A form for creating new users. Includes all the required fields, plus a repeated password. """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,strip=False,
        help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
    email = forms.CharField(max_length=75, required=True)
    subscribe = forms.BooleanField(label="Subscribe to receive emails about projects",required=False)

    def clean_password1(self):
     password1 = self.cleaned_data.get('password1')
     password_validation.validate_password(password1)
     return password1
    def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
            if password1 and password2:
                if password1 != password2:
                    raise forms.ValidationError(
                        self.error_messages['password_mismatch'],
                        code='password_mismatch',
                    )
            return password2


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

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
        subscribe = self.cleaned_data["subscribe"]
        user.type = 3
        print(user.type)
        if commit:
            user.save()
        activation_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
        user.profile.activation_key = activation_key
        user.profile.key_expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        user.profile.save()
        if subscribe:
            subscription = Subscription.objects.create(user=user)
            subscription.save()
        return user



    def __init__(self,*args,**kwargs):
        super(CustomUserStaffCreationForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-personal"
        self.helper.form_method = "POST"
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit','Submit',data_style="expand-right",css_class="pull-right ladda-button btn-primary"))
        self.helper.form_class = 'form-horizontal container'
        self.helper.label_class ="col-sm-3"
        self.helper.field_class = "col-sm-9 "
        self.helper.layout = Layout(
             Field('email', rows="6", css_class='input-xlarge'),
             Field('password1', rows="6", css_class='input-xlarge'),
             Field('password2', rows="6", css_class='input-xlarge'),
             Field('first_name'),
             Field('last_name'),
             Field('subscribe',)

        )

class CustomUserCreationForm(UserCreationForm):
    """ A form for creating new users. Includes all the required fields, plus a repeated password. """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,strip=False,
        help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
    email = forms.CharField(max_length=75, required=True)
    subscribe = forms.BooleanField(label="Subscribe to receive emails about projects",required=False)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ( 'email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password_validation.validate_password(password1)
        return password1
    def clean_password2(self):
                password1 = self.cleaned_data.get('password1')
                password2 = self.cleaned_data.get('password2')
                if password1 and password2:
                    if password1 != password2:
                        raise forms.ValidationError(
                            self.error_messages['password_mismatch'],
                            code='password_mismatch',
                        )
                return password2

    def save(self, commit=True):
        #Save the provided password in hashed format
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        subscribe = self.cleaned_data["subscribe"]
        user.type = 1
        if commit:
            user.save()
        activation_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
        user.profile.activation_key = activation_key
        user.profile.key_expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        user.profile.save()
        if subscribe:
            subscription = Subscription.objects.create(user=user)
            subscription.save()
        return user




    def __init__(self,*args,**kwargs):
        super(CustomUserCreationForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-personal"
        self.helper.form_method = "POST"
        self.helper.form_action = '.'
        self.helper.form_class = 'form-horizontal container'
        self.helper.label_class ="col-sm-3 text-sm-right"
        self.helper.field_class = "col-sm-9 "
        self.helper.layout = Layout(
             Field('email', rows="6", css_class='input-xlarge'),
             Field('password1', rows="6", css_class='input-xlarge'),
             Field('password2', rows="6", css_class='input-xlarge'),
             Field('first_name'),
             Field('last_name'),
             Field('subscribe',),
             Submit('submit','Submit',data_style="expand-right",css_class="pull-right ladda-button btn-primary")

        )

class UserForm(forms.ModelForm):

    class Meta:
     model = User
     fields = ( 'first_name', 'last_name',)

class UserProfileAvatarForm(forms.ModelForm):


    class Meta:
        model = Profile
        fields = ['avatar','resume']

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
        try :
            Subscription.objects.get(user=self.user)
            self.fields['subscribe'].initial=True
        except Subscription.DoesNotExist:
            pass
        self.helper.form_action = '.'
        self.helper.form_class = 'form-horizontal container form-file'
        self.helper.label_class ="col-sm-3 text-sm-right"
        self.helper.field_class = "col-sm-9 "
        self.helper.layout = Layout(
             Field('first_name', rows="6", css_class='input-xlarge'),
             Field('last_name', rows="6", css_class='input-xlarge'),
             Field('avatar',template="user/profile/avatar.html",rows="6", css_class='input-xlarge'),
             Field('resume',template="user/profile/resume.html",rows="6", css_class='input-xlarge'),
             Field('checkbox',template="empty.html"),
             Field('resume_checkbox',template="empty.html"),
             Field('subscribe'),
             Submit('submit','Submit',data_style="expand-right",css_class="ladda-button pull-right btn-primary")
        )
        # define fields order if needed


    def save(self,*args, **kwargs):
        # save both forms
        user = self.uf.save(*args, **kwargs)
        profile = super(UserProfileForm, self).save(*args, **kwargs)
        print("avatar save")
        print(self.__dict__)
        if self.cleaned_data.get("checkbox"):
         profile.avatar = ""
         profile.save()
        if self.cleaned_data.get("resume_checkbox"):
            profile.resume = ""
            profile.save()
        if self.cleaned_data.get("subscribe"):
            subscription = Subscription.objects.get_or_create(user=user)
        else :
            try :
                subscription = Subscription.objects.get(user=self.user)
                subscription.delete()
            except Subscription.DoesNotExist:
                pass
        return profile

    class Meta:
        model = Profile
        fields = ('avatar','resume')
    checkbox = forms.BooleanField(required=False)
    resume_checkbox = forms.BooleanField(required=False)
    subscribe = forms.BooleanField(required=False)

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
        self.helper.form_class = 'form-horizontal container'
        self.helper.label_class ="col-sm-3 text-sm-right"
        self.helper.field_class = "col-sm-9 "
        self.helper.layout = Layout(
             Field('preferences',data_tags="true",data_token_separators="[',']",data_minimum_input_length="0",data_delay="300",multiple="multiple",ajax__cache="true"),
             HTML('<div class="form-group"><div class="control-label col-sm-3"></div><span class="form-text offset-sm-3" style="color:black; font-size:13px;padding-left:10px;" display:inline><span class="badge badge-grey">Grey</span> Approved keywords.<br/> <span class="badge badge-success">Green</span> Users-created keywords.<br/><span class="badge badge-primary">Blue</span> Keywords not created yet</span>'),
             Submit('submit','Submit',data_style="expand-right",css_class="ladda-button btn-primary")
        )
class UserProfilePasswordForm(forms.ModelForm):

    class Meta:
     model = User
     fields = ("last_login",)
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_incorrect': _("Password entered is wrong!")
    }
    passwordcurrent = forms.CharField(label='Password Current', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,strip=False,
        help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput,strip=False)


    def clean_passwordcurrent(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["passwordcurrent"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password_validation.validate_password(password1)
        return password1
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        #Save the provided password in hashed format
        user = super(UserProfilePasswordForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def __init__(self,*args,**kwargs):
        print("passwordForm")
        self.user = kwargs.pop('user')
        super(UserProfilePasswordForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-personal"
        self.helper.form_method = "POST"
        self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal container'
        self.helper.label_class ="col-sm-3 text-sm-right"
        self.helper.field_class = "col-sm-9 "
        self.helper.layout = Layout(
             Field('passwordcurrent', rows="6", css_class='input-xlarge'),
             Field('password1', rows="6", css_class='input-xlarge'),
             Field('password2', rows="6", css_class='input-xlarge'),
             Field('last_login',template="empty.html"),
             Submit('submit','Submit',data_style="expand-right",css_class="ladda-button pull-right btn-primary")
        )

class InterestForm(forms.Form):
   description = forms.CharField(widget=forms.Textarea,required=False,label="Why are your interested in this project?")


class BugForm(forms.Form):
   content = forms.CharField(widget=forms.Textarea,required=True,label="Report Bugs")

class BugWithEmailForm(forms.Form):
   email = forms.EmailField(required=True,label="Email")
   content = forms.CharField(widget=forms.Textarea,required=True,label="Report Bugs")

class UserResendActivationForm(forms.Form):
   def __init__(self,*args,**kwargs):
       super(UserResendActivationForm,self).__init__(*args,**kwargs)
       self.helper = FormHelper(self)
       self.helper.form_id = "id-personal"
       self.helper.form_method = "POST"
       self.helper.form_action = ''
       self.helper.add_input(Submit('submit','Resend Activation Email',data_style="expand-right",css_class="ladda-button btn-primary"))
       self.helper.form_class = 'form-horizontal container'
       self.helper.field_class = "col-sm-12"

class PasswordResetForm(authForms.PasswordResetForm):
        def __init__(self,*args,**kwargs):
            print("passwordForm")
            super(PasswordResetForm,self).__init__(*args,**kwargs)
            self.helper = FormHelper(self)
            self.helper.form_id = "id-personal"
            self.helper.form_method = "POST"
            self.helper.form_action = ''
            #self.helper.add_input(Submit('submit','Submit',data_style="expand-right",css_class="ladda-button pull-right btn-primary"))
            self.helper.form_class = 'form-horizontal container'
            self.helper.label_class ="col-sm-3 text-right"
            self.helper.field_class = "col-sm-9"
            self.helper.layout = Layout(
                 Field('email', rows="6", css_class='input-xlarge'),
                 Div(
                   Submit('submit','Submit',data_style="expand-right",css_class="ladda-button pull-right btn-primary")
                 )
            )


class SetPasswordForm(authForms.SetPasswordForm):
        def __init__(self,*args,**kwargs):
            print("passwordForm")
            super(SetPasswordForm,self).__init__(*args,**kwargs)
            self.helper = FormHelper(self)
            self.helper.form_id = "id-personal"
            self.helper.form_method = "POST"
            self.helper.form_action = ''
            self.helper.add_input(Submit('submit','Submit',data_style="expand-right",css_class="ladda-button btn-primary"))
            self.helper.form_class = 'form-horizontal container'
            self.helper.label_class ="col-sm-3"
            self.helper.field_class = "col-sm-9 "
            self.helper.layout = Layout(
                 Field('new_password1', rows="6", css_class='input-xlarge'),
                 Field('new_password2', rows="6", css_class='input-xlarge'),

            )

class AuthenticationForm(CUserAuthenticationForm):


    def __init__(self, request=None, *args, **kwargs):

        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-personal"
        self.helper.form_method = "POST"
        self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal container'
        self.helper.label_class ="col-sm-3"
        self.helper.field_class = "col-sm-9 "
        self.helper.layout = Layout(
             Field('email', label="Email",rows="6", css_class='input-xlarge'),
             Field('password', rows="6", css_class='input-xlarge'),
             HTML('<div class="col-md-offset-2 .visible-inline-block	" style="padding-left:5px ; display:inline-block"><a  href="/user/password_reset">Forget Password?</a><br><a href="{}" >Have a ucl account? </a></div>'.format(reverse('uclapi:login'))),
             Submit('submit','Submit',data_style="expand-right",css_class="pull-right ladda-button btn-primary")
        )

class ApplyForm(forms.Form):

    first_name = forms.CharField(required=True,max_length=255)
    last_name = forms.CharField(required=True,max_length=255)
    email = forms.CharField(required=True)
    university = forms.CharField(required=True)
    proof = forms.FileField(required=True)

    def __init__(self,*args,**kwargs):
        super(ApplyForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-personal"
        self.helper.form_method = "POST"
        self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal container'
        self.helper.label_class ="col-sm-3"
        self.helper.field_class = "col-sm-9 "
        self.helper.layout = Layout(
           Field('first_name'),
           Field('last_name'),
           Field('email'),
           Field('university'),
           Field('proof'),
           Submit('submit','Submit',data_style="expand-right",css_class="ladda-button btn-primary")
        )
