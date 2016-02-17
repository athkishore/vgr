from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission, Initiative


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

@main.app_context_processor
def inject_initiatives():
    return dict(initiatives=[str(i.name) for i in Initiative.query.order_by('id')])
    