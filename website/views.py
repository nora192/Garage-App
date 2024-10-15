from datetime import datetime, date
from flask import Blueprint, jsonify, render_template, request
import json

from helpers import available_range, generate_available_times, get_available_slots_days, load_slots


views = Blueprint('views', __name__)

# /****************************************************************************************************************/

@views.route("/", methods=['GET'])
def available_slots():
    slots = load_slots()
    today = date.today().isoformat()
    return render_template("slots.html", slots=slots, today=today)

@views.route('/slot-details/<int:slot_id>/<string:date>')
def slot_details(slot_id, date):
    slots = load_slots()
    target_slot = next((slot for slot in slots if slot['slot_id'] == slot_id), None)

    if target_slot:
        available_times = generate_available_times(target_slot, date)
        return render_template("slot-details.html", slot=target_slot, available_times=available_times, date=date)
    
    else:
        return "Slot not found", 404


@views.route("/filter-slots")
def filter_slots():
    slots = load_slots()
    category = request.args.get("category", "all")
    price = request.args.get("price_per_hour", None)
    date_str  = request.args.get("date")
    # use current date incase of no provided date
    date = date_str if date_str else datetime.now().strftime("%Y-%m-%d")

    
    if category != "all":
        slots = [slot for slot in slots if slot['category'] == category]

    slots = get_available_slots_days(slots, date)
    
    if price:
        slots = [slot for slot in slots if slot['price_per_hour'] <= float(price)]
    
    
    return jsonify(slots)



@views.route("/check-range")
def check_range():
    start = request.args.get("start")
    end = request.args.get("end")
    slot_id = request.args.get("slot_id")
    date = request.args.get("date")
    slots = load_slots()

    target_slot = next((slot for slot in slots if slot['slot_id'] == int(slot_id)), None)

    if(available_range(target_slot, date, start, end)):
        return jsonify({"available" : True})
    
    return jsonify({"available" : False})




