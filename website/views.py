from datetime import datetime, date
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session

from helpers import available_range, get_available_slots_days, get_user, load_slots, removeSlotFromSlotsFile, removeSlotFromUserFile, saveBooking
from website.models import Book, Slot


views = Blueprint('views', __name__)


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
        # generate available times for each slot
        slotObj.generate_available_times(date)
        slotsList.append(slotObj.to_dict())

    return jsonify(slotsList)



@views.route("/check-range")
def check_range():
    start = request.args.get("start")
    end = request.args.get("end")
    date = request.args.get("date")
    location = request.args.get("slot_location")
    
    slots = load_slots()
    target_slot = next((slot for slot in slots if slot['location'] == location), None)
    

    if(available_range(target_slot, date, start, end)):
        return jsonify({"available" : True})  # handeled in js
    
    return jsonify({"available" : False}) # handeled in js



@views.route("/book")
def book():

    location = request.args.get("location")
    start = request.args.get("start")
    end = request.args.get("end")
    date = request.args.get("date")
    user_email = session.get('email')
    
    # need to be authenticated
    if 'email' not in session:
        flash("u need to log in first")
        return redirect("/sign-up")
    
    # load slot and find available times
    slots = load_slots()
    target_slot = next((slot for slot in slots if slot['location'] == location), None)
    slot = Slot(location, target_slot['category'], target_slot['price_per_hour'], target_slot['booked_times'])
    slot.generate_available_times(date)

    # check if slot is not booked within that time
    if slot.is_available(date, start, end):
        user = get_user(user_email)
        book = Book(slot, user, date, start, end)
        book.book()


        session['booking'] = {
            'location': slot.location,
            'category': slot.category,
            'price_per_hour': slot.price_per_hour,
            'booked_times' : slot.booked_times,
            'available_times' : slot.available_times,
            'date': date,
            'start': start,
            'end': end,
            'totalPrice': book.totalPrice,
            'user_email': user_email
        }
        
        return render_template("book.html", book = book)
    flash("Slot is already reserved before")
    return redirect("/")


@views.route("/confirm-booking")
def confirmBooking():
    booking = session.get('booking')
    start = int(booking['start'].split(":")[0])
    end = int(booking['end'].split(":")[0])

    saveBooking(booking['location'], booking['user_email'], booking['date'], start, end, booking['category'])
    session['booking'].clear()

    return redirect("/")

@views.route("/profile")
def profile():
    if 'email' not in session:
        return redirect("/sign-up")

    email = session.get('email')
    user = get_user(email)
    return render_template("profile.html", user=user)

@views.route("/cancel-booking")
def cancelBooking():
    location = request.args.get("location")
    start = request.args.get("start")
    end = request.args.get("end")
    date = request.args.get("date")
    email = session.get('email')
    start = int(start)
    end = int(end)

    # remove slot booked time from json file
    if removeSlotFromSlotsFile(location, start, end, date) and removeSlotFromUserFile(email, start, end, location, date):
        flash("deleted successfully", "success")          
        return redirect("/profile")

    flash("failed to delete the slot", "error")          
    return redirect("/profile")


@views.route("/edit", methods=['GET', 'POST'])
def edit():
    if 'email' not in session:
        flash("u need to log in first")
        return redirect("/sign-up")
    
    if request.method == "GET":
        # Get existing booking data
        start = request.args.get("start")
        end = request.args.get("end")
        email = session.get('email')
        location = request.args.get("location")
        date = request.args.get("date")
        category = request.args.get("category")

        slots = load_slots()
        target_slot = None

        for slot in slots:
            if slot['location'] == location:
                target_slot = Slot(location, category, slot['price_per_hour'], slot['booked_times'])
                target_slot.generate_available_times(date)

        if target_slot:
            return render_template("edit.html", slot=target_slot.to_dict(date), start=start, end=end)
        else:
            return "Slot not found", 404 

    elif request.method == "POST":
        location = request.form.get("location")
        new_start = request.form.get("start-time")
        new_end = request.form.get("end-time")
        date = request.form.get("date")
        email = session.get('email')
        category = request.form.get("category")

        slots = load_slots()
        target_slot = next((slot for slot in slots if slot['location'] == location), None)

        old_start = request.form.get("old-start")
        old_end = request.form.get("old-end")

        # Remove the old booking from the slots file and user file
        removeSlotFromSlotsFile(location, int(old_start), int(old_end), date)
        removeSlotFromUserFile(email, int(old_start), int(old_end), location, date)

        # Add new booking
        if available_range(target_slot, date, new_start, new_end):
            saveBooking(location, email, date, int(new_start.split(":")[0]), int(new_end.split(":")[0]), category)
            flash("updated successfully", "success")
            return jsonify({"status": "success", "message": "Booking updated successfully!"})
        else:
            return jsonify({"status": "error", "message": "The selected time range is not available."})
    