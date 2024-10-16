from datetime import datetime, date
from flask import Blueprint, jsonify, render_template, request
import json


# helper function to load data
def load_slots():
    with open('website/static/slots.json', 'r') as f:
        slots = json.load(f)
    return slots

def load_users():
    with open('users.json', 'r') as f:
        users = json.load(f)
    return users

# helper function to get available hours within the day
def generate_available_times(slot, date):
    available_times = []
    booked_times = slot['booked_times'].get(date, [])

    for i in range(1,24):
        time = str(i) + ":00"
        if time not in booked_times:
            available_times.append(time)

    return available_times


# helper function to return available slots in a specific date
def get_available_slots_days(slots, date):
    available_slots = []
    for slot in slots:
        booked_times = slot['booked_times'].get(date, [])
        if len(booked_times) < 24:
            available_slots.append(slot)
    return available_slots


# helper function to check if the given range is available to be booked
def available_range(slot, date, start, end):
    booked_times = slot['booked_times'].get(date, [])
    start_time = int(start.split(":")[0])
    end_time = int(end.split(":")[0])

    for i in range(start_time, end_time):
        str_time = str(i) + ":00"
        if str_time in booked_times:
            return False

    return True

# helper function to save user object in json file
def save_user(user, fileName):
    user_date = user.to_dict()
    try:
        with open(fileName, 'r') as file:
            try:
                users = json.load(file)  
            except json.JSONDecodeError:
                users = []
    except FileNotFoundError:
        users = []
    users.append(user_date)
    with open(fileName, 'w') as file:
        json.dump(users, file, indent=4)


def is_found(email):
    users = load_users()
    for user in users:
        if email == user['email']:
            return True
    return False


def get_user(email):
    users = load_users()
    for user in users:
        if user['email'] == email:
            return user
    return None