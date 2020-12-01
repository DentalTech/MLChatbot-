# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import json


class TimeslotDentistname(Resource):

    def get(self, dentistName):
        print(dentistName)
        print("Time Slot Doctor Name")
        with open('database.txt') as json_file:
            data = json.load(json_file)
            length = len(data['Dentists'])
            print(length)
            for i in range(0, length): 
                if (data['Dentists'][i]["Name"] == dentistName): 
                    print(data['Dentists'][i])
                    return (data['Dentists'][i]), 200

        return [], 404, None