class User:
    firstName=""
    lastName=""
    email=""
    password=""
    phoneNumber=""
    # bookedSlots=[]

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

    