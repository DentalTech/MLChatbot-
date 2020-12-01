# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g, jsonify
import json
from . import Resource
from .. import schemas


class Dentist(Resource):

    def get(self):
        print("Get triggered")
        with open('database.txt') as json_file: 
            data = json.load(json_file)
            dentists = data['Dentists']
            dentists = sorted(data['Dentists'], key=lambda x : x['name'])
            dentists = json.dumps(dentists)
            print(dentists)
            print(json.dumps(data, indent=1))

        return data, 200, None
