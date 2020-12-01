# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.dentist import Dentist
from .api.dentist_dentistName import DentistDentistname


routes = [
    dict(resource=Dentist, urls=['/dentist'], endpoint='dentist'),
    dict(resource=DentistDentistname, urls=['/dentist/<dentistName>'], endpoint='dentist_dentistName'),
]