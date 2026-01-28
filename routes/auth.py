# Basketball Shot Tracker App
# Developed by Christopher Hong
# Team Name: HoopIQ
# Team Members: Christopher Hong, Alfonso Mejia Vasquez, Gondra Kelly, Matthew Margulies, Carlos Orozco
# Start Web Development Date: October 2025
# Finished Web Development Date: June 2026 (Ideally)
# routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash

auth_bp = Blueprint('auth', __name__)

# Login Page
@auth_bp.route("/", methods=["GET"])
def login_page():
    return render_template("login.html", error=None)

# Login action
@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Admin bypass
    if username == "admin" and password == "admin":
        return redirect(url_for("auth.new_page"))

    return render_template("login.html", error="Invalid username or password")

# Register page
@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

# Register action (dummy for now)
@auth_bp.route("/register", methods=["POST"])
def register_user():
    # No real logic yet (will be added later)

    flash("Registration successful! Please log in.")
    return redirect(url_for("auth.login_page"))


# New page after login
@auth_bp.route("/new")
def new_page():
    return render_template("new_page.html")