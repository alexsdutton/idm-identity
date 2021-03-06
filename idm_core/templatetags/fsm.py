from django import template

register = template.Library()


@register.filter('available_state_transitions')
def available_state_transitions(value, arg):
    return {transition.name
            for transition in value.get_available_user_state_transitions(arg)}
