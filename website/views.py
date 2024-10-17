from datetime import datetime, date
from flask import Blueprint, jsonify, render_template, request
import json

from helpers import available_range, generate_available_times, get_available_slots_days, load_slots
from website.models import Slot


views = Blueprint('views', __name__)

# /****************************************************************************************************************/

@views.route("/", methods=['GET'])
def available_slots():
    
    slots = load_slots()
    today = date.today().isoformat()

    slotsList = []
    for slot in slots:
        slotObj = Slot(slot['location'], slot['category'], slot['price_per_hour'], slot['booked_times'])
        slotsList.append(slotObj)



    return render_template("slots.html", slots=slotsList, today=today)


@views.route("/filter-slots")
def filter_slots():
    slots = load_slots()
    category = request.args.get("category", "all")
    price = request.args.get("price_per_hour", None)
    date_str  = request.args.get("date")
    # use current date incase of no provided date
    date = date_str if date_str else datetime.now().strftime("%Y-%m-%d")

    # category filtering
    if category != "all":
        slots = [slot for slot in slots if slot['category'] == category]

    # filter days
    slots = get_available_slots_days(slots, date)
    
    # filter price
    if price:
        slots = [slot for slot in slots if slot['price_per_hour'] <= float(price)]
    

    slotsList = []
    for slot in slots:
        slotObj = Slot(slot['location'], slot['category'], slot['price_per_hour'], slot['booked_times'])
        slotObj.generate_available_times(date)
        slotsList.append(slotObj.to_dict())

    

    return jsonify(slotsList)



@views.route("/check-range")
def check_range():
    start = request.args.get("start")
    end = request.args.get("end")
    # slot_id = request.args.get("slot_id")
    date = request.args.get("date")
    location = request.args.get("slot_location")
    slots = load_slots()

    target_slot = next((slot for slot in slots if slot['location'] == location), None)
    

    if(available_range(target_slot, date, start, end)):
        return jsonify({"available" : True})
    
    return jsonify({"available" : False})




