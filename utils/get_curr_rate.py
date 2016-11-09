

import urllib.request
import json
from django.utils import timezone
from callboard.models import CurrencyRate




CURR = ('USD','EUR')

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def main():

    for c in CURR:
        p = get_html('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=%s&date=%s&json' % (c, timezone.now().strftime('%Y%m%d')))
        p1 = p.decode('utf-8')
        rate = json.loads(p1)[0]['rate']
        print(c+' курс '+str(rate))
        CurrencyRate.objects.update_or_create(
        currency=c, defaults={'rate': rate})

if __name__ == "__main__":

        main()