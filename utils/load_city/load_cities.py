__author__ = 'okorablev'

import csv
from django.test import TestCase
from userprofile.models import Cities,States
import os

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sxodu.settings")

workpath = os.path.dirname(os.path.abspath(__file__))


def load():

    # file = open(os.path.join(workpath, 'cities'))
    # reader = csv.reader(file, delimiter=';')

    cities_list = parse()

    for city in cities_list:
       citys = city.split(':')
       state = States.objects.get(pk=int(citys[0]))
       model = Cities(state=state,city=citys[1])


       model.save()

def parse():
    file = open(os.path.join(workpath, 'cities_all'))
    reader = csv.reader(file, delimiter=',')
    l=list()
    for line in reader:
        line4 = line[3]

        for d in ' \')':
            line4 = line4.replace(d,'')

        line2=int(line[2].replace(' ',''))


        l.append(str(line2)+':'+line4)


    file.close()
    return l