from django import template
from django.db.models import Max
from threadedcomments.models import ThreadedComment
register = template.Library()


def last_comment(object):



    lasn_num = ThreadedComment.objects.filter(object_pk=object).aggregate(Max('pk'))
    if  lasn_num['pk__max'] == None:
        res = ''
        return res
    else:
        res = str(lasn_num['pk__max'])
    return res
    #replace the messages_set with the appropriate related_name, and also the filter field. (I am assuming it to be "read")

register.filter(last_comment)