from django.test import TestCase, RequestFactory
from ..models import Keyword,Project,Organization
from cuser.models import CUser as User
import datetime

class KeywordModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Keyword.objects.create(title="Test Keyword",type=1,status=True)

    def test_title_label(self):
        keyword = Keyword.objects.get(id=1)
        field_label = keyword._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'title')

    def test_type_label(self):
        keyword = Keyword.objects.get(id=1)
        field_label = keyword._meta.get_field('type').verbose_name
        self.assertEquals(field_label,'type')

    def test_status_label(self):
        keyword = Keyword.objects.get(id=1)
        field_label = keyword._meta.get_field('status').verbose_name
        self.assertEquals(field_label,'status')


class ProjectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.organization = Organization.objects.create(title="UCL",status=True)
        cls.organization.save()
        user = User.objects.create_user(email="siewml9512223@gmail.")
        Project.objects.create(title="Test Project",summary="testing project",slug="test-project",organization=cls.organization,created_by=user,deadline=datetime.datetime.now())

    def test_title_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'title')

    def test_summary_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'title')

    def test_slug_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('slug').verbose_name
        self.assertEquals(field_label,'slug')


    def test_organization_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('organization').verbose_name
        self.assertEquals(field_label,'organization')

    def test_created_by_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('created_by').verbose_name
        self.assertEquals(field_label,'created by')

    def test_updated_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('updated').verbose_name
        self.assertEquals(field_label,'updated')

    def test_timestamp_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('deadline').verbose_name
        self.assertEquals(field_label,'deadline')

    def test_keywords_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('keywords').verbose_name
        self.assertEquals(field_label,'keywords')

    def test_title_max_length(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('title').max_length
        self.assertEquals(max_length,250)
