from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.core.mail import EmailMultiAlternatives
from djmatch.views import send_mail
from ..models import  Interest, Profile,Invitation
from project.models import Project,Keyword
from django.db.models import Q,Count
import itertools , operator
from  functools import reduce
from django.template import loader

def sendInterest(request):
    if request.user.is_authenticated and request.GET["id"]:
       if request.user.profile.is_verified == False:
           response = JsonResponse({"error" : "Must have a verified account!"})
           response.status_code = 403
           return response
       if request.user.profile.type == 3:
           response = JsonResponse({"error" : "Must hava a student account!"})
           response.status_code = 403
           return response
       try:
         project = Project.objects.get(pk=request.GET["id"])
         if project.created_by != request.user:
            flag = Interest.objects.get(user=request.user,project=project)
         else:
          response = JsonResponse({"error" : "Cannot be interest in your own project"})
          response.status_code = 403
          return response

       except Interest.DoesNotExist:
                 Interest.objects.create(user=request.user,project=project,description=request.GET["description"])
                 try :
                   send_notification(request)
                 except:
                    response = JsonResponse({"error" : "Error in sending mail!"})
                    response.status_code = 403
                    return response
                 count = Interest.objects.filter(project=request.GET["id"]).count()
                 return JsonResponse({"interest": [],"amount":count})
       except Project.DoesNotExist:
          response = JsonResponse({"error" : "The project do not exists"})
          response.status_code = 403
          return response
       response = JsonResponse({"error" : "You already done it"})
       response.status_code = 403
       return response
    else :
       response = JsonResponse({"error" : "Must be log in"})
       response.status_code = 403
       return response

def send_notification(request):
    if request.user.is_authenticated and (request.user.profile.type == 2 or request.user.profile.type == 1) :
        user = request.user
        project_id = request.GET["id"]
        project = Project.objects.all().get(pk=project_id)
        if project_id:
            subject = "You have received a notificaion from {}.".format("Notice Project")
            message = "Dear Sir/Madam\n I am writing this email to inform you that I am interested in this project\n\n Project Name : {} \n Email: {}\n".format(project.title,project.created_by.email)
            from_email = 'contact.dataspartan@gmail.com'
            to_email = [project.created_by.email]
            send_mail(subject,message,from_email,to_email,fail_silently=False)
        else:
            return None
    else:
        return None

def sendBug(request):
    if request.user.is_authenticated:
        user = request.user
        email = user.email
        content = request.GET["content"]
        if email:
            subject = "Contact : {}.".format(email)
            message = "Dear Sir/Madam\nemail: {}\ncontent : \n{}\n".format(email,content)
            from_email = 'siewml95@gmail.com'
            to_email = 'contact.dataspartan@gmail.com'
            send_mail(from_email,to_email,subject,message)
            #send_mail(subject,message,from_email,to_email,fail_silently=False)
            return JsonResponse({})
        else:
              response = JsonResponse({"error" : "Some Error Occured"})
              response.status_code = 403
              return response
    else:
        content = request.GET["content"]
        email = request.GET["email"]
        if email:
            subject = "Contact : {}.".format(email)
            message = "Dear Sir/Madam\n Email: {}\n content : \n {}\n".format(email,content)
            from_email = 'contact.dataspartan@gmail.com'
            to_email = [user.email]
            send_mail(subject,message,from_email,to_email,fail_silently=False)
            return JsonResponse({})
        else:
            response = JsonResponse({"error" : "Some Error Occured"})
            response.status_code = 403
            return response
def getIndexRecommendations(request):
    if request.user.is_authenticated:
      interests = Interest.objects.filter(user=request.user)
      preferences = request.user.profile.preferences.active()
      q_expressions = [[keyword.id for keyword in interest.project.keywords.active()] for interest  in interests]
      q_list =  set(itertools.chain.from_iterable(q_expressions))
      p_list = set([x.id for x in preferences])
      q_list_exclude = [x for x in q_list if x not in p_list]
      q_expressions = [Q(keywords=keyword) for keyword in q_list_exclude]
      p_expressions = [Q(keywords=keyword) for keyword in p_list]
      current_project_id = request.GET["id"]
      if current_project_id == 0 or current_project_id == "0":
        interested = [interest.project.id for interest in interests]
      else:
        interested = [interest.project.id for interest in interests]
        interested.append(current_project_id)
      if p_expressions != []:
       p = Project.objects.published().filter(reduce(operator.or_,p_expressions)).exclude(created_by=request.user).exclude(id__in=interested)
      else:
       p = []
      if q_expressions != []:
        q = Project.objects.published().filter(reduce(operator.or_,q_expressions)).exclude(created_by=request.user).exclude(id__in=interested)
      else:
        q = []
      if p != []:
        t = p.values("pk","slug","title").annotate(keyword_count=Count("keywords")).order_by('-keyword_count')[0:10]
      else:
        t = []
      if  q != []:
       k = q.values("pk","slug","title").annotate(keyword_count=Count("keywords")).order_by('-keyword_count')[0:10]
      else:
       k = []
      factor = 2
      final = []
      m = list(k)
      length = len(k) - 1
      if len(t) != 0 and len(k) == 0:
          for item in t:
              item['keyword_count'] *= factor
          k = t
      else:
          for index_t,item_t in enumerate(t):
             for index_k,item_k in enumerate(k):
                 if index_k == length:
                             final.append(item_t)
                             break
                 elif item_t['pk'] == item_k['pk']:
                             m[index_k]["keyword_count"] += item_t['keyword_count'] * factor
                             break
          k = (m + final)
      k = sorted(k,key=lambda x: x["keyword_count"],reverse=True)[0:10]
      return JsonResponse({"recommendations": list(k)})
    else :
      return JsonResponse({"recommendations": []})

def sendActivationEmail(activation_key,email_target):
        html_message = loader.render_to_string(
            'user/activation_email.html',
            {
                'message': 'Dear Sir/Madam\nPlease click the link below to verify your account',
                'link' : activation_key,
            }
        )
        text_content = 'Text'


        subject = "You have received a notificaion from {}.".format("Notice Project")
        from_email = 'contact.dataspartan@gmail.com'
        to_email = [email_target]
        #send_mail(subject,'message',from_email,to_email,fail_silently=False)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_message, "text/html")
        msg.send()
