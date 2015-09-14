from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from wagtail.wagtailcore.rich_text import expand_db_html
from django.template.loader_tags import do_include
from django.template.defaulttags import CommentNode


from core.snippets import NavigationMenu
from core.utilities import *

register = template.Library()


@register.filter
def raw(value):
    if value is not None:
        html = expand_db_html(value)
    else:
        html = ''

    return mark_safe(html)


@register.filter
def content_type(model):
    """
    Return the model name/"content type" as a string e.g BlogPage, NewsListingPage.
    Can be used with "slugify" to create CSS-friendly classnames
    Usage: {% raw %}{{ self|content_type|slugify }} {% endraw %}
    """
    return model.__class__.__name__


@register.inclusion_tag('core/includes/menu.html', takes_context=True)
def navigation_menu(context, menu_name=None, current_page=None):
    """
    Retrieves the MenuElement(s) under the NavigationMenu with given menu_name
    """
    menu_items = []
    if menu_name is None or current_page is None:
        return None
    try:
        menu_items = NavigationMenu.objects.get(menu_name=menu_name).items
    except ObjectDoesNotExist:
        return None

    return {
        'links': menu_items,
        'request': context['request'],
    }


@register.inclusion_tag('core/includes/menu_small.html', takes_context=True)
def navigation_menu_small(context, menu_name=None, current_page=None):
    """
    Retrieves the MenuElement(s) under the NavigationMenu with given menu_name
    """
    menu_items = []
    if menu_name is None or current_page is None:
        return None
    try:
        menu_items = NavigationMenu.objects.get(menu_name=menu_name).items
    except ObjectDoesNotExist:
        return None

    return {
        'links': menu_items,
        'request': context['request'],
    }


class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""


@register.tag(name='set')
def set_var(parser, token):
    """
    Usage: {% set var_name  = var_value %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set var_name  = var_value %}")
    return SetVarNode(parts[1], parts[3])


@register.tag('include_optional')
def do_include_maybe(parser, token):
    "Source: http://stackoverflow.com/a/18951166/15690"
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError(
            "%r tag takes at least one argument: "
            "the name of the template to be included." % bits[0])

    try:
        silent_node = do_include(parser, token)
    except template.TemplateDoesNotExist:
        # Django < 1.7
        return CommentNode()

    _orig_render = silent_node.render

    def wrapped_render(*args, **kwargs):
        try:
            return _orig_render(*args, **kwargs)
        except template.TemplateDoesNotExist:
            return CommentNode()
    silent_node.render = wrapped_render
    return silent_node


@register.simple_tag
def get_param_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()