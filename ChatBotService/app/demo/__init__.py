# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask, render_template

import v1


def create_app():
    app = Flask(__name__, static_folder='static')
    app.register_blueprint(
        v1.bp)
    return app

if __name__ == '__main__':
    create_app().run(host="0.0.0.0", port="5005", debug=True)