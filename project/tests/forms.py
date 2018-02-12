from ..forms import ProjectModelForm,ProjectFilterForm
from django.test import TestCase, RequestFactory
from cuser.models import CUser as User
import datetime

class ProjectModelFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email="siewml9512223@gmail.")
    def test_title_required(self):
        user = User.objects.get(id=1)

        form = ProjectModelForm(data={'summary':"test summary","slug":"test-summary","company":"UCL","created_by":user,"deadline":datetime.datetime.now()})
        self.assertEquals(form.is_valid(),False)

    def test_summary_required(self):
        user = User.objects.get(id=1)
        form = ProjectModelForm(data={'title':'test',"slug":"test-summary","company":"UCL","created_by":user,"deadline":datetime.datetime.now()})
        self.assertEquals(form.is_valid(),False)

    def test_company_required(self):
        user = User.objects.get(id=1)
        form = ProjectModelForm(data={'title':'test','summary':"test summary","slug":"test-summary","created_by":user,"deadline":datetime.datetime.now()})
        self.assertEquals(form.is_valid(),False)

    def test_deadline_required(self):
        user = User.objects.get(id=1)
        form = ProjectModelForm(data={'title':'test','summary':"test summary","slug":"test-summary","created_by":user,"company":"UCL"})
        self.assertEquals(form.is_valid(),False)

class ProjectModelUpdateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email="siewml9512223@gmail.")
    def test_title_required(self):
        user = User.objects.get(id=1)

        form = ProjectModelForm(data={'summary':"test summary","slug":"test-summary","company":"UCL","created_by":user,"deadline":datetime.datetime.now()})
        self.assertEquals(form.is_valid(),False)

    def test_summary_required(self):
        user = User.objects.get(id=1)
        form = ProjectModelForm(data={'title':'test',"slug":"test-summary","company":"UCL","created_by":user,"deadline":datetime.datetime.now()})
        self.assertEquals(form.is_valid(),False)

    def test_company_required(self):
        user = User.objects.get(id=1)
        form = ProjectModelForm(data={'title':'test','summary':"test summary","slug":"test-summary","created_by":user,"deadline":datetime.datetime.now()})
        self.assertEquals(form.is_valid(),False)

    def test_deadline_required(self):
        user = User.objects.get(id=1)
        form = ProjectModelForm(data={'title':'test','summary':"test summary","slug":"test-summary","created_by":user,"company":"UCL"})
        self.assertEquals(form.is_valid(),False)
