from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def format_advice(value):
    # # Convert headers
    # value = re.sub(r'#### (.*)', r'<h4>\1</h4>', value)
    # value = re.sub(r'### (.*)', r'<h3>\1</h3>', value)
    
    # # Convert bullet points
    # value = re.sub(r'^- (.*)', r'<li>\1</li>', value, flags=re.M)
    # value = value.replace('<li>', '<ul><li>').replace('</li>', '</li></ul>')
    # value = value.replace('</ul><ul>', '')  # Fix consecutive lists
    
    # # Convert bold text
    # value = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', value)
    
    # # Convert horizontal rules
    # value = value.replace('---', '<hr>')
    
    # # Preserve line breaks
    # value = value.replace('\n\n', '<br>')
    
    return mark_safe(value)