from flask import request, make_response
import mysql.connector
import re # Regular expressions also called Regex
from functools import wraps
from datetime import datetime

############################## CONNECTION TO THE DATABASE
# Creates and returns a connection to the database.
def db():
    try:
        db = mysql.connector.connect(
            host = "mariadb",
            user = "root",  
            password = "password",
            database = "2026_1_travel"
        )
        cursor = db.cursor(dictionary=True)
        return db, cursor
    except Exception as e:
        print(e, flush=True)
        raise Exception("Database under maintenance", 500)


############################## DECORATOR - NO CACHE
# Decorator that tells the browser never to cache the page. 
# Every time the route is visited, the browser must fetch a fresh copy from the server instead of using a saved version.
def no_cache(view):
    @wraps(view)
    def no_cache_view(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return no_cache_view


############################## VALIDATING USER FIRST NAME
USER_FIRST_NAME_MIN = 2
USER_FIRST_NAME_MAX = 20
# Regex says: Must be between 2 and 20 characters and can only contain letters, spaces, apostrophes and hyphens.
REGEX_USER_FIRST_NAME = f"^[a-zA-ZÀ-ÖØ-öø-ÿ\\s'\\-]{{{USER_FIRST_NAME_MIN},{USER_FIRST_NAME_MAX}}}$"
def validate_user_first_name():
    user_first_name = request.form.get("user_first_name", "").strip()
    if not re.match(REGEX_USER_FIRST_NAME, user_first_name):
        raise Exception("company_exception user_first_name")
    return user_first_name

############################## VALIDATING USER LAST NAME
USER_LAST_NAME_MIN = 2
USER_LAST_NAME_MAX = 20
REGEX_USER_LAST_NAME = f"^[a-zA-ZÀ-ÖØ-öø-ÿ\\s'\\-]{{{USER_LAST_NAME_MIN},{USER_LAST_NAME_MAX}}}$"
def validate_user_last_name():
    user_last_name = request.form.get("user_last_name", "").strip()
    if not re.match(REGEX_USER_LAST_NAME, user_last_name):
        raise Exception("company_exception user_last_name")
    return user_last_name

############################## VALIDATING USER EMAIL
REGEX_USER_EMAIL = "^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"
def validate_user_email():
    user_email = request.form.get("user_email", "").strip()
    if not re.match(REGEX_USER_EMAIL, user_email):
        raise Exception("company_exception user_email")
    return user_email

############################## VALIDATING USER PASSWORD
USER_PASSWORD_MIN = 8
USER_PASSWORD_MAX = 50
REGEX_USER_PASSWORD = f"^.{{{USER_PASSWORD_MIN},{USER_PASSWORD_MAX}}}$"
def validate_user_password():
    user_password = request.form.get("user_password", "").strip()
    if not re.match(REGEX_USER_PASSWORD, user_password):
        raise Exception("company_exception user_password")
    return user_password

############################## COUNTRIES ARRAY FOR TRAVEL FORM
COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
    "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada",
    "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros",
    "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark",
    "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador",
    "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji",
    "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece",
    "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras",
    "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel",
    "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati",
    "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia",
    "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi",
    "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania",
    "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia",
    "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal",
    "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea",
    "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama",
    "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal",
    "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia",
    "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
    "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore",
    "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea",
    "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland",
    "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo",
    "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu",
    "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States",
    "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam",
    "Yemen", "Zambia", "Zimbabwe"
]

############################## VALIDATING TRAVEL LOCATION
TRAVEL_LOCATION_MIN = 2
TRAVEL_LOCATION_MAX = 50
REGEX_TRAVEL_LOCATION = f"^.{{{TRAVEL_LOCATION_MIN},{TRAVEL_LOCATION_MAX}}}$"
def validate_travel_location():
    travel_location = request.form.get("travel_location", "").strip()
    if not re.match(REGEX_TRAVEL_LOCATION, travel_location):
        raise Exception("company_exception travel_location")
    return travel_location

############################## VALIDATING TRAVEL TITLE
TRAVEL_TITLE_MIN = 2
TRAVEL_TITLE_MAX = 50
REGEX_TRAVEL_TITLE = f"^.{{{TRAVEL_TITLE_MIN},{TRAVEL_TITLE_MAX}}}$"
def validate_travel_title():
    travel_title = request.form.get("travel_title", "").strip()
    if not re.match(REGEX_TRAVEL_TITLE, travel_title):
        raise Exception("company_exception travel_title")
    return travel_title

############################## VALIDATING TRAVEL DATES
def validate_travel_dates():
    travel_arrival_date = request.form.get("travel_arrival_date", "")
    travel_departure_date = request.form.get("travel_departure_date", "")
    
    if not travel_arrival_date: raise Exception("company_exception travel_arrival_date")
    if not travel_departure_date: raise Exception("company_exception travel_departure_date")
    
    arrival = datetime.strptime(travel_arrival_date, "%Y-%m-%d")
    departure = datetime.strptime(travel_departure_date, "%Y-%m-%d")
    
    if departure < arrival: raise Exception("company_exception travel_departure_before_arrival")
    
    return travel_arrival_date, travel_departure_date