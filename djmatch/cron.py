from django_cron import CronJobBase, Schedule
from user.models import Subscription,Interest
from project.models import Project
import datetime,itertools,operator
from django.core.mail import send_mass_mail
from django.db.models import Q,Count
from  functools import reduce

def getIndexRecommendations(user):
          print("getIndexRecommendations")
          print(user)
          interests = Interest.objects.filter(user=user)
          preferences = user.profile.preferences.active()
          print(preferences)
          q_expressions = [[keyword.id for keyword in interest.project.keywords.active()] for interest  in interests]
          q_list =  set(itertools.chain.from_iterable(q_expressions))
          p_list = set([x.id for x in preferences])
          print("fuck")
          q_list_exclude = [x for x in q_list if x not in p_list]
          print(q_list_exclude)
          print(p_list)
          q_expressions = [Q(keywords=keyword) for keyword in q_list_exclude]
          print(q_expressions)
          p_expressions = [Q(keywords=keyword) for keyword in p_list]
          print(q_expressions)
          print(p_expressions)
          interested = [interest.project.id for interest in interests]

          if p_expressions != []:
           p = Project.objects.published().filter(reduce(operator.or_,p_expressions)).exclude(created_by=user).exclude(id__in=interested)
          else:
           p = []
          if q_expressions != []:
            q = Project.objects.published().filter(reduce(operator.or_,q_expressions)).exclude(created_by=user).exclude(id__in=interested)
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
          print('factor')
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
          print("k")
          print(list(k))
          return list(k)
class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'djmatch.MyCronJob'    # a unique code

    def do(self):
      print("bitch")
      subscriptions = Subscription.objects.filter(user__profile__is_verified=True)
      final_email = ()
      print(subscriptions)
      for subscription in subscriptions:
          print(subscription)
          temp = getIndexRecommendations(subscription.user)
          print(temp)
          if temp != []:
              string = ""
              print(string)
              for x in temp:
                  print(x)
                  string += "Project Title : {} \n".format((x["title"]))
                  print(string)
              print(string)

              final_email += (("subject ",string,'contact.dataspartan@gmail.com',[subscription.user.email])),
              print(final_email)
      print("send_mass_mail")
      print(final_email)
      send_mass_mail(final_email)
