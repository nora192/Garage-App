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

    # def book(self, date, start, end):

    #     self.bookedSlots.append(slot)

class Slot:
    def __init__(self, location, category, price_per_hour, booked_times):
        self.location = location
        self.category = category
        self.price_per_hour = price_per_hour
        self.booked_times = booked_times  # Dictionary of booked times by date
        self.available_times = []

    def generate_available_times(self, date=None):
        """Generate available times for a specific date based on booked times."""
        if date is None:
            today = datetime.today()
            date = today.strftime('%Y-%m-%d')

        self.available_times = []

        all_times = [f"{i}:00" for i in range(1, 24)]
        
        booked_for_date = self.booked_times.get(date, [])

        self.available_times = [time for time in all_times if time not in booked_for_date]

        return self.available_times

    def to_dict(self, date=None):
        """Return the slot information as a dictionary, including available times."""
        return {
            'location': self.location,
            'category': self.category,
            'price_per_hour': self.price_per_hour,
            'booked_times': self.booked_times,
            'available_times': self.available_times
        }

    def book(self, date, time):
        """Book a slot at a specific date and time."""
        if date not in self.booked_times:
            self.booked_times[date] = []
        self.booked_times[date].append(time)
    
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
    

