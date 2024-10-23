# Garage Slot Parking

The Garage Slot Parking Web Application is designed to simplify the process of finding and booking parking slots.
- What does it do? 
  Example:This application aims to enhance the parking experience by providing a user-friendly interface and efficient search functionalities.
- What is the "new feature" which you have implemented that we haven't seen before?  
  Search Functionality: Users can search for available parking slots based on:
  Category: Filter slots by vehicle category (SUV, compact, motorcycle, truck).
  Price: Set a price range to find slots that fit their budget.
  Date: Select a date to view available slots for specific timeframes.
  Booking Management: Users can view, edit, or cancel their booked slots.

## Prerequisites
Did you add any additional modules that someone needs to install (for instance anything in Python that you `pip install-ed`)? 
List those here (if any).

Before running this project, ensure you have the following prerequisites installed:

- Python: Install Python from the official website: python.org
- Flask: You can install Flask using pip, Python's package installer. Run the following command:
` pip install Flask`
- Jinja: Jinja is a templating engine used by Flask, and it should be integrated into Visual Studio Code by default when you have the Python extension installed.
- Flask_session
`pip install flask_session`

## Project Checklist
- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
- [x] It uses at least one module from the Python Standard Library other than the random module.
      Please provide the name of the module you are using in your app.
  - Module name: json, datetime
- [x] It contains at least one class written by you that has both properties and methods. It uses `__init__()` to let the class initialize the object's attributes (note that `__init__()` doesn't count as a method). This includes instantiating the class and using the methods in your app. Please provide below the file name and the line number(s) of at least one example of a class definition in your code as well as the names of two properties and two methods.
  - File name for the class definition: "website\models.py"
  - Line number(s) for the class definition: 4, 30, 91
  - Name of two properties: User(email, firstName, lastName, phoneNumber, password), Slot(location, category, price_per_hour, booked_times)
  - Name of two methods: Slot.generate_available_times(date=None), Slot.is_available(self, date, start, end)
  - File name and line numbers where the methods are used: 49, 96 @"views.py"
- [x] It makes use of JavaScript in the front end and uses the localStorage of the web browser.
- [x] It uses modern JavaScript (for example, let and const rather than var).
- [x] It makes use of the reading and writing to the same file feature.
- [x] It contains conditional statements. Please provide below the file name and the line number(s) of at least
      one example of a conditional statement in your code.
  - File name: "helpers.py"
  - Line number(s): 40
- [x] It contains loops. Please provide below the file name and the line number(s) of at least
      one example of a loop in your code.
  - File name: helpers.py
  - Line number(s): 77
- [x] It lets the user enter a value in a text box at some point.
      This value is received and processed by your back end Python code.
- [x] It doesn't generate any error message even if the user enters a wrong input.
- [x] It is styled using CSS.
- [x] The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code.
      In particular, the code should not use `print()` or `console.log()` for any information the app user should see. Instead, all user feedback needs to be visible in the browser.
- [x] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.
