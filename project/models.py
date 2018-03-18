from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils import timezone
from .utils import unique_slug_generator
from cuser.models import CUser as User
import datetime
# Create your models here.

class OrganizationQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=True)
    def inactive(self):
        return self.filter(status=False)


class OrganizationManager(models.Manager):
    def get_queryset(self):
        return OrganizationQuerySet(self.model,using=self._db)

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()
class ProjectQuerySet(models.QuerySet):
    def published(self):
        #return self.filter(status=2,deadline__lte=datetime.datetime.now())
        return  self.filter(status=2,deadline__gte=datetime.datetime.now())

class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model,using=self._db)

    def published(self):
        return self.get_queryset().published()


class KeywordQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=True)

    def inactive(self):
        return self.filter(status=False)


class KeywordManager(models.Manager):
    def get_queryset(self):
        return KeywordQuerySet(self.model,using=self._db)

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        print("keyword requirement manager")
        return self.get_queryset().inactive()


class Organization(models.Model):
     title = models.CharField(max_length=120,unique=True)
     type = models.IntegerField(default=1)
     status = models.BooleanField(default=False)
     objects = OrganizationManager()

     def __str__(self):
         return self.title

class Keyword(models.Model):
     title = models.CharField(max_length = 120,unique=True)
     type = models.IntegerField(default=1)
     status = models.BooleanField(default=False)

     objects = KeywordManager()
     def __str__(self):
         return self.title

class Project(models.Model):
    STATUS_CHOICES = (
            (1, 'Draft'),
            (2, 'Active'),
            (3, 'Taken'),
            (4, 'Completed'),
    )
    #user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    title = models.CharField(max_length=250,blank=False)
    slug = models.SlugField(unique=True,blank=False)
    summary = models.TextField(blank=False)
    organization = models.ForeignKey(Organization,default=None,null=True)
    status = models.IntegerField(choices=STATUS_CHOICES,default=1)
    image = models.FileField(blank=True,null=True)
    #publish = models.DateField(auto_now=False,auto_now_add=False)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    deadline = models.DateField(auto_now=False,auto_now_add=False)
    keywords = models.ManyToManyField(Keyword)
    url = models.URLField(null=True,blank=True)
    created_by = models.ForeignKey(User,default=1)
    objects = ProjectManager()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #return reverse("project:detail",kwargs={"slug":self.slug})
        return "/project"

    def status_verbose(self):
        return dict(Project.STATUS_CHOICES)[self.status]

def pre_save_post_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_post_receiver,sender=Project)
