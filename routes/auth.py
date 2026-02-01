# Basketball Shot Tracker App
# Developed by Christopher Hong
# Team Name: HoopIQ
# Team Members: Christopher Hong, Alfonso Mejia Vasquez, Gondra Kelly, Matthew Margulies, Carlos Orozco
# Start Web Development Date: October 2025
# Finished Web Development Date: June 2026 (Ideally)
# routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
import plotly.graph_objects as go
from plotly.io import to_html
import numpy as np, math

# Temporary shot data (will move later)
# Temporary shot data for testing
shots_data = [
    {"shot_id": 1, "backboard": False, "rim": False, "net_only": True, "made": True,
     "top_x": [0,1,2], "top_y": [0,10,20], "side_x": [0,1,2], "side_y": [0,5,10]},
    {"shot_id": 2, "backboard": True, "rim": False, "net_only": False, "made": True,
     "top_x": [0,1,2], "top_y": [0,8,15], "side_x": [0,1,2], "side_y": [0,4,9]},
    {"shot_id": 3, "backboard": False, "rim": True, "net_only": False, "made": False,
     "top_x": [0,1,2], "top_y": [0,9,18], "side_x": [0,1,2], "side_y": [0,6,12]}
]

def generate_top_view(shots, selected_idx):
    fig = go.Figure()

    # Half-court size
    court_width, court_length = 50, 29  # half court

    # Court outline
    fig.add_shape(type="rect", x0=-court_width/2, y0=0, 
                  x1=court_width/2, y1=court_length,
                  line=dict(color="gray", width=2))

    # Backboard at bottom
    backboard_y = 3  
    backboard_width = 6
    fig.add_shape(type="line",
                  x0=-backboard_width/2, y0=backboard_y,
                  x1=backboard_width/2, y1=backboard_y,
                  line=dict(color="black", width=3))

    # Rim
    rim_y = backboard_y + 1.25  
    rim_diameter = 1.5
    fig.add_shape(type="circle",
                  x0=-rim_diameter/2, y0=rim_y - rim_diameter/2,
                  x1=rim_diameter/2, y1=rim_y + rim_diameter/2,
                  line=dict(color="red", width=3))

    # Paint/key area
    key_width, key_length = 12, 18
    key_x0, key_x1 = -key_width/2, key_width/2
    key_y0, key_y1 = 0, key_length
    fig.add_shape(type="rect",
                  x0=key_x0, y0=key_y0,
                  x1=key_x1, y1=key_y1,
                  line=dict(color="orange", width=2))
    
    # Free throw circle (top half)
    theta = np.linspace(0, math.pi, 50)
    arc_radius = 6
    arc_x = arc_radius * np.cos(theta)
    arc_y = key_length + arc_radius * np.sin(theta)  
    fig.add_trace(go.Scatter(x=arc_x, y=arc_y, mode='lines', line=dict(color="orange"), showlegend=False))

    # 3-point line (arc and corners)
    radius_3pt = 19.75
    rim_center_x, rim_center_y = 0, rim_y
    theta = np.linspace(0, math.pi, 100)
    arc3_x = rim_center_x + radius_3pt * np.cos(theta)
    arc3_y = rim_center_y + radius_3pt * np.sin(theta)
    corner_limit = 19.75
    arc3_x = np.clip(arc3_x, -corner_limit, corner_limit)
    fig.add_trace(go.Scatter(x=arc3_x, y=arc3_y, mode='lines', line=dict(color="orange", width=2), showlegend=False))
    fig.add_shape(type="line", x0=-corner_limit, y0=0, x1=-corner_limit, y1=arc3_y[0], line=dict(color="orange", width=2))
    fig.add_shape(type="line", x0=corner_limit, y0=0, x1=corner_limit, y1=arc3_y[-1], line=dict(color="orange", width=2))

    # Add shots
    for i in selected_idx:
        shot = shots[i]
        color = "green" if shot['made'] else "red"
        fig.add_trace(go.Scatter(x=shot['top_x'], y=shot['top_y'],
                                 mode='lines+markers', line=dict(color=color, width=3),
                                 marker=dict(size=6),
                                 name=f"Shot {i+1}"))

    # Layout adjustments
    fig.update_layout(title="Top View of Ball Trajectory (High-School Court)",
                      autosize=True,
                      xaxis=dict(range=[-26, 26], scaleanchor="y", scaleratio=1),
                      yaxis=dict(range=[0, 30]),
                      height=500)
    
    return to_html(fig, full_html=False)

def generate_side_view(shots, selected_idx):
    fig = go.Figure()
    for i in selected_idx:
        shot = shots[i]
        color = "green" if shot['made'] else "red"
        fig.add_trace(go.Scatter(
            x=shot["side_x"], y=shot["side_y"],
            mode="lines+markers",
            line=dict(color=color, width=3),
            marker=dict(size=6),
            name=f"Shot {i+1}"
        ))
    return to_html(fig, full_html=False)

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
    made_shots = sum(1 for s in shots_data if s["made"])
    backboard_hits = sum(1 for s in shots_data if s["backboard"])
    rim_hits = sum(1 for s in shots_data if s["rim"])
    net_only = sum(1 for s in shots_data if s["net_only"])

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