from django import template
from ..forms import  BugForm
register = template.Library()
@register.simple_tag
def bug_form():
    return BugForm()
