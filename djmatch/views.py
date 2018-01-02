from django_select2.views import AutoResponseView
from django.http import JsonResponse

class NewView(AutoResponseView):
    def get(self, request, *args, **kwargs):
        self.widget = self.get_widget_or_404()
        self.term = kwargs.get('term', request.GET.get('term', ''))
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse({
            'results': [
                {
                    'text': self.widget.label_from_instance(obj),
                    'id': obj.pk,
                    'type' : obj.type
                }
                for obj in context['object_list']
                ],
            'more': context['page_obj'].has_next()
        })
