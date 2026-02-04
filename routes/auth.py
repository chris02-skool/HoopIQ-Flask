# Basketball Shot Tracker App
# Developed by Christopher Hong
# Team Name: HoopIQ
# Team Members: Christopher Hong, Alfonso Mejia Vasquez, Gondra Kelly, Matthew Margulies, Carlos Orozco
# Start Web Development Date: October 2025
# Finished Web Development Date: June 2026 (Ideally)
# routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from services.trajectory import generate_top_view, generate_side_view
import csv
from io import StringIO
from services.export import export_session_csv
from datetime import datetime


# Temporary shot data (will move later)
# Temporary shot data for testing
shots_data = [
    {"top_x":[0,1,0,0], "top_y":[25,18,12,4.25], "side_x":[25,20,10,4.5], "side_y":[6,12,11,10], "result":"Make",
     "Backboard":1, "Rim":1, "Net":0},
    {"top_x":[0,2,1,0], "top_y":[25,17.5,11,4.25], "side_x":[25,20,10,4.5], "side_y":[6,13,11,10], "result":"Make",
     "Backboard":0, "Rim":0, "Net":1},
    {"top_x":[0,0,0,0], "top_y":[25,18,12,4.25], "side_x":[25,20,10,4.5], "side_y":[6,15,13,10], "result":"Make",
     "Backboard":1, "Rim":0, "Net":1},
    {"top_x":[0,-2,-3,-3], "top_y":[25,17,12,6], "side_x":[25,20,10,4.5], "side_y":[6,9,8,4], "result":"Miss",
     "Backboard":1, "Rim":1, "Net":0},
    {"top_x":[0,1,2,3], "top_y":[25,18,13,7], "side_x":[25,20,10,4.5], "side_y":[6,9,8,5], "result":"Miss",
     "Backboard":0, "Rim":1, "Net":0},
    {"top_x":[0,-1,-0.5,0], "top_y":[25,19,13,4.25], "side_x":[25,20,10,4.5], "side_y":[6,10,11,10], "result":"Make",
     "Backboard":0, "Rim":0, "Net":1},
    {"top_x":[0,-1,-2,-2.5], "top_y":[25,18,13,6], "side_x":[25,20,10,4.5], "side_y":[6,8,8,4], "result":"Miss",
     "Backboard":0, "Rim":1, "Net":0},
    {"top_x":[0,-2,-1,0], "top_y":[25,17,10,4.25], "side_x":[25,20,10,4.5], "side_y":[6,13,12,10], "result":"Make",
     "Backboard":1, "Rim":0, "Net":1},
    {"top_x":[0,2,3,3], "top_y":[25,19,14,6], "side_x":[25,20,10,4.5], "side_y":[6,8,7,4], "result":"Miss",
     "Backboard":0, "Rim":1, "Net":0},
    {"top_x":[0,0,1,2], "top_y":[25,18,14,6], "side_x":[25,20,10,4.5], "side_y":[6,8,7,4], "result":"Miss",
     "Backboard":1, "Rim":1, "Net":0}
]

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

# New Page after login
@auth_bp.route("/new")
def new_page():
    # 1️⃣ Stats calculations
    total_shots = len(shots_data)
    made_shots = sum(1 for s in shots_data if s["result"] == "Make")
    backboard_hits = sum(1 for s in shots_data if s["Backboard"])
    rim_hits = sum(1 for s in shots_data if s["Rim"])
    net_only = sum(1 for s in shots_data if s["Net"] and not s["Rim"] and not s["Backboard"])

    # 2️⃣ Trajectory graphs
    selected_idx = list(range(len(shots_data)))  # show all shots for now
    top_graph = generate_top_view(shots_data, selected_idx)
    side_graph = generate_side_view(shots_data, selected_idx)

    # 3️⃣ Pass everything to the template
    return render_template(
        "new_page.html",
        shots=shots_data,
        total_shots=total_shots,
        made_shots=made_shots,
        backboard_hits=backboard_hits,
        rim_hits=rim_hits,
        net_only=net_only,
        top_graph=top_graph,
        side_graph=side_graph
    )

@auth_bp.route("/export/session")
def export_session():
    # For now, pass shots_data and session datetime (replace later with real session)
    session_datetime = datetime(2026, 2, 4, 11, 30)
    return export_session_csv(shots_data, session_datetime)