from datetime import datetime, date
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session
import json

from helpers import available_range, get_available_slots_days, get_user, load_slots, removeSlotFromSlotsFile, removeSlotFromUserFile, saveBooking
from website.models import Book, Slot, User


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


@views.route("/book")
def book():

    location = request.args.get("location")
    start = request.args.get("start")
    end = request.args.get("end")
    date = request.args.get("date")
    user_email = request.args.get("email")

    slots = load_slots()
    
    target_slot = next((slot for slot in slots if slot['location'] == location), None)
    
    slot = Slot(location, target_slot['category'], target_slot['price_per_hour'], target_slot['booked_times'])

    user = get_user(user_email)

    book = Book(slot, user, date, start, end)
    book.book()


    session['booking'] = {
        'location': slot.location,
        'category': slot.category,
        'price_per_hour': slot.price_per_hour,
        'booked_times' : slot.booked_times,
        'date': date,
        'start': start,
        'end': end,
        'totalPrice': book.totalPrice,
        'user_email': user['email']
    }
    
    return render_template("book.html", book = book)


@views.route("/confirm-booking")
def confirmBooking():
    booking = session.get('booking')

    start = int(booking['start'].split(":")[0])
    end = int(booking['end'].split(":")[0])

    saveBooking(booking['location'], booking['user_email'], booking['date'], start, end, booking['category'])

    return redirect("/")

@views.route("/profile")
def profilr():
    email = session.get('email')
    user = get_user(email)
    return render_template("profile.html", user=user)

@views.route("/cancel-booking")
def cancelBooking():
    location = request.args.get("location")
    start = request.args.get("start")
    end = request.args.get("end")
    date = request.args.get("date")
    email = request.args.get("email")
    start = int(start)
    end = int(end)

    # remove slot booked time from json file
    if removeSlotFromSlotsFile(location, start, end, date) and removeSlotFromUserFile(email, start, end, location, date):
        flash("deleted successfully", "success")          
        return redirect("/profile")

    flash("failed to delete the slot", "error")          
    return redirect("/profile")
         



    








    
    
    

    



    


