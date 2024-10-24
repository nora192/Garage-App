from datetime import datetime
from datetime import datetime

class User:
    firstName=""
    lastName=""
    email=""
    password=""
    phoneNumber=""
    bookedSlots=[]
    

    def __init__(self, email, firstName, lastName, phoneNumber, password):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.phoneNumber = phoneNumber
        self.password = password

    # a function to convert user object to a dictionary so it can be added to the json file
    def to_dict(self):
        return {
            'email': self.email,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'phoneNumber': self.phoneNumber,
            'password': self.password
        }

class Slot:
    def __init__(self, location, category, price_per_hour, booked_times):
        self.location = location
        self.category = category
        self.price_per_hour = price_per_hour
        self.booked_times = booked_times  # Dictionary of booked times by date
        self.available_times = {}

    def generate_available_times(self, date=None):
        """Generate available times for a specific date based on booked times."""
        today = datetime.today().strftime('%Y-%m-%d')

        all_times = [f"{i}:00" for i in range(1, 24)]
        
        # Initialize available_times as a dictionary
        self.available_times = {'start': [], 'end': []}

        if date == today:
            # Check time only if the date is today
            time_now = datetime.now().hour
            booked_for_date = self.booked_times.get(date, {'start': [], 'end': []})
            
            self.available_times['start'] = [
                time for time in all_times 
                if time not in booked_for_date['start'] and int(time.split(":")[0]) > time_now
            ]
            self.available_times['end'] = [
                time for time in all_times 
                if time not in booked_for_date['end'] and int(time.split(":")[0]) > time_now
            ]

        else:
            booked_for_date = self.booked_times.get(date, {'start': [], 'end': []})
            
            self.available_times['start'] = [
                time for time in all_times if time not in booked_for_date['start']
            ]
            self.available_times['end'] = [
                time for time in all_times if time not in booked_for_date['end']
            ]

        return self.available_times

    def to_dict(self, date=None):
        """Return the slot information as a dictionary, including available times."""
        return {
            'location': self.location,
            'category': self.category,
            'price_per_hour': self.price_per_hour,
            'booked_times': self.booked_times,
            'available_times': self.available_times,
            'date': date
        }

    def is_available(self, date, start, end):
        times = self.generate_available_times(date)
        for i in range(int(start.split(":")[0]), int(end.split(":")[0]) + 1):
            if f"{i}:00" not in times['start'] and f"{i}:00" not in times['end']:
                return False
        return True

class Book:


    def __init__(self, slot, user, date, start, end):
        self.slot = slot
        self.user = user
        self.date = date
        self.start = start
        self.end = end
    
    def book(self):
        startInt = int(self.start.split(":")[0])
        endInt = int(self.end.split(":")[0])            
        self.totalPrice = (endInt - startInt) * self.slot.price_per_hour
    

