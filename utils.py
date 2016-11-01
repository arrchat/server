import base64
import os
import datetime

__author__ = 'JuniorJPDJ'


def random_string(length):
    if length < 10:
        tmplength = 10
    else:
        tmplength = length
    str = base64.urlsafe_b64encode(os.urandom(int(tmplength*0.76)))[:-2]
    return str[:length]


def datetime_to_timestamp(time):
    return int((time - datetime.datetime(1970, 1, 1)).total_seconds())
