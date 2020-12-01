# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.timeslot import Timeslot
from .api.timeslot_dentistName import TimeslotDentistname


routes = [
    dict(resource=Timeslot, urls=['/timeslot'], endpoint='timeslot'),
    dict(resource=TimeslotDentistname, urls=['/timeslot/<dentistName>'], endpoint='timeslot_dentistName'),
]