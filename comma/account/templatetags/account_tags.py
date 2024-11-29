from django import template
from django.urls import reverse
from django.templatetags.static import static

register = template.Library()

@register.inclusion_tag('partials/activity_icon.html')
def activity_icon():
    return {
        'activity_url': reverse('account:activity'),
        'get_count_url': reverse('account:get_new_activities_count'),
        'activity_js': static('js/activity.js')
    }