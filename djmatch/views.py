from __future__ import print_function
import httplib2,os
from django_select2.views import AutoResponseView
from django.http import JsonResponse
import boto3
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import ContactForm
from django.template import loader
from .utils import send_mail
import os

from apiclient import errors
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


class NewView(AutoResponseView):
    def get(self, request, *args, **kwargs):
        self.widget = self.get_widget_or_404()
        self.term = kwargs.get('term', request.GET.get('term', ''))
        self.object_list = self.get_queryset().active()
        context = self.get_context_data()
        x = {
            'results': [
                {
                    'text': self.widget.label_from_instance(obj),
                    'id': obj.pk,
                    'type' : obj.type
                }
                for obj in context['object_list']
                ],
            'more': context['page_obj'].has_next()
        }
        print(x)
        return JsonResponse(x)


def sign_s3(request):
  S3_BUCKET = settings.AWS_STORAGE_BUCKET_NAME

  file_name = request.GET["file_name"]
  file_type = request.GET["file_type"]

  s3 = boto3.client('s3',
       aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
  )

  presigned_post = s3.generate_presigned_post(
    Bucket = S3_BUCKET,
    Key = file_name,
    Fields = {"acl": "public-read", "Content-Type": file_type},
    Conditions = [
      {"acl": "public-read"},
      {"Content-Type": file_type}
    ],
    ExpiresIn = 3600
  )

  return JsonResponse({
    'data': presigned_post,
    'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
  })


class IndexView(TemplateView):
    template_name="index.html"
    title = "Home"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["title"] = self.title
        return context

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '.'

    def form_valid(self, form):
        html_message = loader.render_to_string(
            'email/contact.html',
            {
                'message': self.request.POST["message"],
                'name' : self.request.POST["name"],
                'email' : self.request.POST["email"]
            }
        )

        subject = "Contact Message"
        from_email = settings.EMAIL_HOST_USER
        to_email = settings.EMAIL_HOST_USER
        send_mail(subject,html_message,from_email,to_email,html=True)
        return super().form_valid(form)
