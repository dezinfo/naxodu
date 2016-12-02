from userprofile.models import UserProfileTable
from django.utils.timezone import now

class SetLastVisitMiddleware(object):
    def process_response(self, request, response):
        if request.user.is_authenticated():
            # Update last visit time after request finished processing.
            try:
                UserProfileTable.objects.filter(username=request.user).update(last_visit=now())
            except:
                pass
        return response