from datetime import datetime, timedelta
import random
from flask import Blueprint, jsonify, render_template
import json

views = Blueprint('views', __name__)

# helper function to load data
def load_slots():
    with open('website/static/slots.json', 'r') as f:
        slots = json.load(f)
    return slots


# helper function to get available datetime
def generate_available_times(slot, days_in_advance=7):
    available_times = {}
    booked_times = slot.get('booked_times', {})

    for i in range(days_in_advance):
        day = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        if day not in booked_times:
            available_times[day] = random.sample(["09:00", "10:00", "11:00", "12:00", "13:00", "14:00"], 3)
        else:
            # Get times that are not already booked
            available_times[day] = [time for time in ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00"] 
                                    if time not in booked_times[day]]

    return available_times


@views.route("/")
def home():
    return "here is the home page"

@views.route("/available-slots", methods=['GET'])
def available_slots():
    slots = load_slots()
    return render_template("slots.html", slots=slots)



@views.route('/slot-details/<int:slot_id>')
def slot_details(slot_id):
    slots = load_slots()
    target_slot = next((slot for slot in slots if slot['slot_id'] == slot_id), None)
    if target_slot:
        available_times = generate_available_times(target_slot)

        return render_template("slot-details.html", slot=target_slot, available_times=available_times)
    else:
        return "Slot not found", 404



