from flask import Blueprint

user = Blueprint('user', __name__, url_prefix='/user')

import palisade.ui.user.views