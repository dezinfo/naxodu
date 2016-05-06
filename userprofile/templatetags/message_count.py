

from django import template

register = template.Library()


def unread_messages(user):
    return user.inbox_set.filter(status='Unread').count()
    #replace the messages_set with the appropriate related_name, and also the filter field. (I am assuming it to be "read")

register.filter(unread_messages)

