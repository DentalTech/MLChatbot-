# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import json

class DentistDentistname(Resource):

    def get(self, dentistName):
        print("Dentist Name Triggered")
        print(dentistName)
        with open('database.txt') as json_file: 
            data = json.load(json_file)
            print(json.dumps(data))
            for i in data['Dentists']:
                print(i)
                if (i["name"] == dentistName):
                    x = json.dumps(i)
                    return x, 200, None
            else: 
                return None, 404, None 
         