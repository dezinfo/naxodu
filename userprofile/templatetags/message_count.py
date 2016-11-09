

from django import template

register = template.Library()


def unread_messages(user):
    return user.inbox_set.filter(status='Unread').count()
    #replace the messages_set with the appropriate related_name, and also the filter field. (I am assuming it to be "read")

def user_name(username):

    return username[0].capitalize()

register.filter(unread_messages)
register.filter(user_name)

