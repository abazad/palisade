from flask import Blueprint

admin = Blueprint('admin', __name__, url_prefix='/admin')

import palisade.ui.admin.views

