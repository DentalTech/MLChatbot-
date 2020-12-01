# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from .wit import ask_wit


class Input(Resource):

     def post(self):
        message = request.form['my-message']
        print(message)
        answer = ask_wit(message)
        print(answer)

        return answer, 200, None