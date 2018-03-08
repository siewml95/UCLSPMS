import django_tables2 as tables
from project.models import Project
from .models import Interest
from django_tables2.utils import A

class UserProfileProjectTable(tables.Table):
    status = tables.Column(attrs={'th':{'class': 'w-25'},'td':{'class':'col-25'}},orderable=False)
    title = tables.LinkColumn(args=[A('pk')],attrs={'th':{'class': 'w-75'},'td':{'class':'col-75'}},orderable=False)
    timestamp = tables.DateColumn(attrs={'th':{'class': 'w-25'},'td':{'class':'col-25'}},orderable=False)

    class Meta:
        model = Project
        fields = ('status','title','timestamp')
        attrs = {'thead': {'class' : 'table-color'}}

class UserProfileStaffInterestTable(tables.Table):
    user = tables.Column(attrs={'th':{'class': 'w-25'},'td':{'class':'col-25'}},orderable=False)
    project = tables.Column(attrs={'th':{'class': 'w-75'},'td':{'class':'col-75'}},orderable=False)
    timestamp = tables.DateColumn(attrs={'th':{'class': 'w-25'},'td':{'class':'col-25'}},orderable=False)

    class Meta:
        model = Interest
        fields = ('user','project','timestamp')
        attrs = {'thead': {'class' : 'table-color'}}


class UserProfileInterestTable(tables.Table):
    project = tables.Column(attrs={'th':{'class': 'w-75'},'td':{'class':'col-75'}},orderable=False)
    timestamp = tables.DateColumn(attrs={'th':{'class': 'w-25'},'td':{'class':'col-25'}},orderable=False)

    class Meta:
        model = Interest
        fields = ('project','timestamp')
        attrs = {'thead': {'class' : 'table-color'}}
