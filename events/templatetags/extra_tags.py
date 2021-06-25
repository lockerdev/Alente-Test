from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def get_username_from_userid(user_id):
    try:
        return User.objects.get(id=user_id).username
    except User.DoesNotExist:
        return 'Unknown'

@register.filter
def addstr(arg1, arg2):
    return str(arg1) + str(arg2)

@register.filter
def remove_slash(arg1):
    return str(arg1).replace('/')

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()