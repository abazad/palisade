from flask import Blueprint

wpump = Blueprint('wpump', __name__, url_prefix='/wpump')

import palisade.ui.wpump.views