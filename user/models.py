from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from project.models import Project,Keyword
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.core.mail import EmailMultiAlternatives
from djmatch.utils import send_mail
from django.utils.translation import ugettext_lazy as _
from cuser.models import CUser as User
from django.conf import settings
from django.template import loader

class InterestQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=True)

    def inactive(self):
        return self.filter(status=False)


class InterestManager(models.Manager):
    def get_queryset(self):
        return InterestQuerySet(self.model,using=self._db)

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()

class ProfileManager(models.Manager):
    pass

class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    status = models.BooleanField(default=False)
    objects = InterestManager()


class Invitation(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Inactive'),
        (3, 'Done'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(blank=False)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES)
    objects = InterestManager()


    def __str__(self):
            return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.IntegerField(default=1)
    birth_date = models.DateField(null=True, blank=True)
    preferences = models.ManyToManyField(Keyword)
    avatar = models.FileField(blank=True, null=True)
    resume = models.FileField(blank=True,null=True)
    linkedin = models.URLField(blank=True)
    activation_key = models.CharField(max_length=40,blank=True)
    key_expires = models.DateTimeField(blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    objects = models.Manager()

class Subscription(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)


@receiver(post_save,sender=Invitation)
def create_invitation(sender,instance,created,**kwargs):
  if created:
        html_message = loader.render_to_string(
            'user/activation_email.html',
            {
                'message': 'Dear Sir/Madam\n This is the link to create a staff account',
                'link' : "{}/user/invitation/{}".format(settings.SITE_URL,instance.id),
            }
        )
        text_content = 'Text'
        subject = "You have received a notificaion from {}.".format("Notice Project")
        from_email = settings.EMAIL_HOST_USER
        to_email = instance.email
        send_mail(subject,html_message,from_email,to_email,html=True)
        '''msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_message, "text/html")
        msg.send()'''


@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        try:
         if instance.type == 2:
                profile  = Profile.objects.create(user=instance,type=2)
                print("profile")
                print(profile.profile)
         elif instance.type == 3:
                profile  = Profile.objects.create(user=instance,type=3)
         else:
              print("type == 1")
              Profile.objects.create(user=instance,type=1)
        except:
              Profile.objects.create(user=instance,type=1)



@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
