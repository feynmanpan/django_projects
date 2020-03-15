from django import template
register = template.Library()


#register.filter('mrp', filter_my_replace)
@register.filter
def url_amp(urlstr):
    """Removes all values of arg from the given string""" 
    return urlstr.replace('&amp;', '&')


@register.filter
def author(authorstr):
    authorstr=authorstr.replace("_","：")
    return authorstr


@register.filter(name='my_filter1')
def filter_my_replace(value):
    """Removes all values of arg from the given string""" 
    return value.replace('2', '1')
	
@register.filter
def my_filter2(value,arg):
    """Removes all values of arg from the given string""" 
    return arg