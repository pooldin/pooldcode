from flask import Blueprint, render_template
from pooldcode.auth import requires_auth

plan = Blueprint('index', __name__)


@plan.route('/', methods=['GET'])
@requires_auth
def root():
    return render_template('index.html')
