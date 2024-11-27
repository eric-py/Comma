from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.inclusion_tag('partials/comment_section.html')
def render_comment_section(comments):
    return {'comments': comments}