from flask import Blueprint, jsonify, render_template
import json

views = Blueprint('views', __name__)


def load_slots():
    with open('website/static/slots.json', 'r') as f:
        slots = json.load(f)
    return slots



@views.route("/")
def home():
    return "here is the home page"

@views.route("/available-slots", methods=['GET'])
def available_slots():
    slots = load_slots()
    return render_template("slots.html", slots=slots)

@views.route('/slot-details/<int:slot_id>')
def slot_details(slot_id):
    # your logic here
    return "here is the slot details"


