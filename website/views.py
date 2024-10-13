from flask import Blueprint

views = Blueprint('views', __name__)


@views.route("/")
def home():
    return "here is the home page"

@views.route("/available-slots")
def available_slots():
    return "here is the available slots"

