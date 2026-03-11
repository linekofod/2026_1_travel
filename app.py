from flask import Flask, render_template, request, jsonify, session, redirect
import x
import uuid
import time
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
 
from icecream import ic
ic.configureOutput(prefix=f'-------- | ', includeContext=True)
 
app = Flask(__name__)
 
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


############################## SHOW TRAVEL DESTINATIONS PAGE (INDEX)
@app.get("/")
@x.no_cache
def show_index():
    try:
        user = session.get("user", "") # Gets user key from session (logged in). If not logged in it returns an empty string
        db, cursor = x.db()

        if not user: return redirect("/login") # If there is no logged-in user, redirect to login page.

        # If logged-in user exists in the session
        # It runs the database query to fetch all travel destinations belonging to that user, and stores the results in travels.
        else: 
            q = "SELECT * FROM travel_destinations WHERE user_fk = %s ORDER BY travel_created_at DESC"
            cursor.execute(q, (user["user_pk"],))
            travels = cursor.fetchall()

        # Renders the page_index and passes the user, x file, travels and title of the page
        return render_template("page_index.html", user=user, x=x, travels=travels, title="Travel Destinations")
    except Exception as ex:
        ic(ex)
        return "ups"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


############################## SHOW SIGNUP PAGE
@app.get("/signup")
@x.no_cache
def show_signup():
    try:
        user = session.get("user", "")
        return render_template("page_signup.html", hide_nav=True, user=user, x=x, title="Signup")
    except Exception as ex:
        ic(ex)
        return "ups"


############################## CREATE A NEW USER
@app.post("/api-create-user")
def api_create_user():
    try:
        # Validating user
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        user_hashed_password = generate_password_hash(user_password)
        # ic(user_hashed_password) # the hashed password in the terminal: 'scrypt:32768:8:1$laHJGKP9gkvUGTKY$4681b30032148b07b0905c803595df806662cce02a2503a8ed1247665cd42e4db163fad94f7c6e38e4e84462901e6f712673b2de6d15f3a39d2072584f31b4d5'

        user_pk = uuid.uuid4().hex # Generates a unique id with uuid
        user_created_at = int(time.time()) # Gets the current time and converts it to an integer (EPOCH)

        db, cursor = x.db() # Connects to the database
        q = "INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s);" # Creates a query
        cursor.execute(q, (user_pk, user_first_name, user_last_name, user_email, user_hashed_password, user_created_at)) # Executes the query
        db.commit() # Saves (commit) the changes to the database

        form_signup = render_template("___form_signup.html", x=x) # Render the form_signup

        # Replaces the form on the page with the form_signup component (empty form), then redirect to the login page.
        return f"""
        <browser mix-replace="form">{form_signup}</browser>
        <browser mix-redirect="/login"></browser>
        """

    except Exception as ex:
        ic(ex)
        # If the first name validation failed, show an error tooltip telling the user the allowed length, using the validation variables from the x file.
        if "company_exception user_first_name" in str(ex):
            error_message = f"User first name {x.USER_FIRST_NAME_MIN} to {x.USER_FIRST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_last_name" in str(ex):
            error_message = f"User last name {x.USER_LAST_NAME_MIN} to {x.USER_LAST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_email" in str(ex):
            error_message = f"User email invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_password" in str(ex):
            error_message = f"User password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400
        
        if "Duplicate entry" in str(ex) and "user_email" in str(ex):
            error_message = "Email already exists"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


############################## SHOW LOGIN PAGE
@app.get("/login")
@x.no_cache
def show_login():
    try:
        user = session.get("user", "")
        if not user: # If there's no user, the login page is shown ("hide_nav=True" hides the nav)
            return render_template("page_login.html", hide_nav=True, user=user, x=x, title="Login")
        return redirect("/") # If there is a user and your logged in, the index page (travel destinations) is shown
    except Exception as ex:
        ic(ex)
        return "ups"


############################## LOGIN ROUTE
@app.post("/api-login")
def api_login():
    try:
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()

        # If no user found - returns an error tooltip "Invalid credentials"
        if not user:
            error_message = "Invalid credentials"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400
        
        # If password doesn't match - compares the submitted password against the hashed password in the DB, and returns "Invalid credentials" if wrong
        if not check_password_hash(user["user_password"], user_password): # Checks if the password exists by comparing the user_password in the database with the user_password in typed in the input field
            error_message = "Invalid credentials"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        user.pop("user_password") # Removes the password from showing in the session
        session["user"] = user # Saves the user to the session

        return f"""<browser mix-redirect="/"></browser>""" # Redirects to the index page if the user is succesfully logged in

    except Exception as ex:
        ic(ex)
        if "company_exception user_email" in str(ex):
            error_message = f"User email invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_password" in str(ex):
            error_message = f"User password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


############################## LOGOUT ROUTE
@app.get("/logout")
def logout():
    try:
        session.clear()
        return redirect("/login")
    except Exception as ex:
        ic(ex)
        return "ups"


############################## SHOW CREATE TRAVEL PAGE
@app.get("/create-travel")
@x.no_cache
def show_create_travel():
    try:
        user = session.get("user", "")
        return render_template("page_create_travel.html", user=user, x=x, title="Create travel destination")
    except Exception as ex:
        ic(ex)
        return "ups"


############################## CREATE A NEW TRAVEL
@app.post("/api-create-travel")
def api_create_travel():
    try:
        user = session.get("user", "")

        travel_country = request.form.get("travel_country", "")
        travel_location = x.validate_travel_location()
        travel_title = x.validate_travel_title()
        travel_description = request.form.get("travel_description", "").strip()
        travel_arrival_date, travel_departure_date = x.validate_travel_dates()

        travel_pk = uuid.uuid4().hex
        travel_created_at = int(time.time())

        db, cursor = x.db()

        q = "INSERT INTO travel_destinations VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(q, (travel_pk, travel_country, travel_location, travel_title, travel_description, travel_arrival_date, travel_departure_date, user["user_pk"], travel_created_at))
        db.commit()

        form_create_travel = render_template("___form_create_travel.html", x=x)

        return f"""
        <browser mix-replace="form">{form_create_travel}</browser>
        <browser mix-redirect="/"></browser>
        """

    except Exception as ex:
        ic(ex)

        if "company_exception travel_location" in str(ex):
            error_message = f"Travel location {x.TRAVEL_LOCATION_MIN} to {x.TRAVEL_LOCATION_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception travel_title" in str(ex):
            error_message = f"Travel title {x.TRAVEL_TITLE_MIN} to {x.TRAVEL_TITLE_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception travel_arrival_date" in str(ex):
            error_message = "Please add an arrival date"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception travel_departure_date" in str(ex):
            error_message = "Please add a departure date"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400
            
        if "company_exception travel_departure_before_arrival" in str(ex):
            error_message = "Departure date should be later than arrival date"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


############################## SHOW UPDATE TRAVEL PAGE
@app.get("/update-travel/<travel_pk>")
@x.no_cache
def show_update_travel(travel_pk):
    try:
        user = session.get("user", "")
        db, cursor = x.db()
        q = "SELECT * FROM travel_destinations WHERE travel_pk = %s"
        cursor.execute(q, (travel_pk,))
        travel = cursor.fetchone()
        return render_template("page_update_travel.html", user=user, x=x, travel=travel, title="Update travel destination")
    except Exception as ex:
        ic(ex)
        return "ups"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


############################## UPDATING A TRAVEL
@app.patch("/api-update-travel/<travel_pk>")
def api_update_travel(travel_pk):
    try:
        parts = [] # Stores "field = %s" strings
        values = [] # Stores the actual values

        # For each field, we check if the user filled it in. 
        # If the field has a value it gets updated, otherwise it gets skipped entirely
        travel_country = request.form.get("travel_country", "").strip()
        if travel_country:
            parts.append("travel_country = %s")
            values.append(travel_country)

        travel_location = x.validate_travel_location()
        if travel_location:
            parts.append("travel_location = %s")
            values.append(travel_location)

        travel_title = x.travel_title()
        if travel_title:
            parts.append("travel_title = %s")
            values.append(travel_title)

        travel_description = request.form.get("travel_description", "").strip()
        if travel_description:
            parts.append("travel_description = %s")
            values.append(travel_description)

        travel_arrival_date, travel_departure_date = x.validate_travel_dates()
        if travel_arrival_date:
            parts.append("travel_arrival_date = %s")
            values.append(travel_arrival_date)
        if travel_departure_date:
            parts.append("travel_departure_date = %s")
            values.append(travel_departure_date)

        # If no fields were provided at all, return a 400 error instead of running an empty query.
        if not parts: return "nothing to update", 400

        values.append(travel_pk) # Add the travel_pk to values

        partial_query = ", ".join(parts) # Join the parts list into a string

        q = f"UPDATE travel_destinations SET {partial_query} WHERE travel_pk = %s" # Creates the query

        # Connects to the database and executes the query with the new values
        db, cursor = x.db()
        cursor.execute(q, values)
        db.commit()

        return f"""
        <browser mix-redirect="/"></browser>
        """

    except Exception as ex:
        print(ex)
        return str(ex), 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


############################## SHOWING MORE INFORMATION FROM TRAVEL
@app.get("/show-more-travel/<travel_pk>")
def show_more_travel(travel_pk):
    try:
        user = session.get("user", "")
        db, cursor = x.db()
        q = "SELECT * FROM travel_destinations WHERE travel_pk = %s" 
        cursor.execute(q, (travel_pk,))
        travel = cursor.fetchone()
        return render_template("page_show_more_travel.html", user=user, x=x, travel=travel)
    except Exception as ex:
        print(ex, flush=True)
        return "ups", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


############################## DELETING A TRAVEL
@app.delete("/api-delete-travel/<travel_pk>")
def api_delete_travel(travel_pk):
    try:
        db, cursor = x.db()
        q = "DELETE FROM travel_destinations WHERE travel_pk = %s"
        cursor.execute(q, (travel_pk,))
        db.commit()
        return f"""
            <browser mix-remove="#travel-{travel_pk}">
            </browser>
        """
    except Exception as ex:
        ic(ex)
        return str(ex)
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()