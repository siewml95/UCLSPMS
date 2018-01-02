from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils import timezone
from .utils import unique_slug_generator
from django.contrib.auth.models import User

# Create your models here.

class ProjectQuerySet(models.QuerySet):
    def published(self):
        return self.filter(draft=False)

class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model,using=self._db)

    def published(self):
        return self.get_queryset().published()


class KeywordQuerySet(models.QuerySet):
    def common(self):
        return self.filter(status=False,type=1)

    def requirement(self):
        return self.filter(status=False,type=2)


class KeywordManager(models.Manager):
    def get_queryset(self):
        return KeywordQuerySet(self.model,using=self._db)

    def common(self):
        return self.get_queryset().common()

    def requirement(self):
        print("keyword requirement manager")
        return self.get_queryset().requirement()

class Keyword(models.Model):
     title = models.CharField(max_length = 120,unique=True)
     type = models.IntegerField(default=1)
     status = models.BooleanField(default=False)

     objects = KeywordManager()
     def __str__(self):
         return self.title

class Project(models.Model):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    title = models.CharField(max_length=250,blank=False)
    slug = models.SlugField(unique=True,blank=False)
    summary = models.TextField(blank=False)
    company = models.CharField(max_length=250,blank=False)
    draft = models.BooleanField(default=False)

    #publish = models.DateField(auto_now=False,auto_now_add=False)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    deadline = models.DateField(auto_now=False,auto_now_add=False)
    keywords = models.ManyToManyField(Keyword)
    created_by = models.ForeignKey(User,default=1)
    objects = ProjectManager()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #return reverse("project:detail",kwargs={"slug":self.slug})
        return "/project"

def pre_save_post_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_post_receiver,sender=Project)
