# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Blueprint, render_template
import flask_restful as restful

from .routes import routes
from .validators import security


@security.scopes_loader
def current_scopes():
    return []

bp = Blueprint('v1', __name__, static_folder='static', template_folder='templates')
api = restful.Api(bp, catch_all_404s=True)

@bp.route('/')
def index():
    return render_template("index.html")
for route in routes:
    api.add_resource(route.pop('resource'), *route.pop('urls'), **route)