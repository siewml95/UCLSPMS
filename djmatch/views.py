from django_select2.views import AutoResponseView
from django.http import JsonResponse
import boto3
from django.conf import settings
from django.views.generic import TemplateView

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
