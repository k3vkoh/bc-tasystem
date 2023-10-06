from django import template

register = template.Library()

@register.filter
def bootstrap(field):
    return field.as_widget(attrs={"class": "form-control"})
