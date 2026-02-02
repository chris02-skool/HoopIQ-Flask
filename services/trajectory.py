# Basketball Shot Tracker App
# Developed by Christopher Hong
# Team Name: HoopIQ
# Team Members: Christopher Hong, Alfonso Mejia Vasquez, Gondra Kelly, Matthew Margulies, Carlos Orozco
# Start Web Development Date: October 2025
# Finished Web Development Date: June 2026 (Ideally)
# services/trajectory.py

import plotly.graph_objects as go
from plotly.io import to_html
import numpy as np, math

def generate_top_view(shots, selected_idx):
    """
    Generates a top-view basketball court with a placeholder trajectory.
    """

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
        color = "green" if shot['result'] == "Make" else "red"
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
    """
    Generates a top-view basketball court with a placeholder trajectory.
    """

    fig = go.Figure()

    # Canonical HS Geometry
    HALF_COURT_X = 50

    BACKBOARD_X = 3             
    BACKBOARD_WIDTH = 0.1       
    BACKBOARD_HEIGHT = 3.5
    RIM_HEIGHT = 10
    RIM_DIAMETER = 1.5          
    RIM_OFFSET_FROM_BACKBOARD = 1.25  

    FLOOR_Y = 0

    # Floor
    fig.add_shape(
        type="line",
        x0=-5, y0=FLOOR_Y,
        x1=HALF_COURT_X, y1=FLOOR_Y,
        line=dict(color="black", width=2)
    )

    # Half-court line
    fig.add_shape(
        type="line",
        x0=HALF_COURT_X, y0=0,
        x1=HALF_COURT_X, y1=16,
        line=dict(color="gray", width=2, dash="dash")
    )
    fig.add_annotation(
        x=HALF_COURT_X, y=16,
        text="Half Court Line",
        showarrow=False,
        yshift=10,
        font=dict(color="gray")
    )

    # Backboard
    backboard_bottom_y = RIM_HEIGHT - 1.5
    backboard_top_y = backboard_bottom_y + BACKBOARD_HEIGHT

    fig.add_shape(
        type="line",
        x0=BACKBOARD_X, y0=backboard_bottom_y,
        x1=BACKBOARD_X, y1=backboard_top_y,
        line=dict(color="black", width=3)
    )
    

    # Rim
    rim_x_left = BACKBOARD_X + RIM_OFFSET_FROM_BACKBOARD - RIM_DIAMETER/2
    rim_x_right = BACKBOARD_X + RIM_OFFSET_FROM_BACKBOARD + RIM_DIAMETER/2

    fig.add_shape(
        type="line",
        x0=rim_x_left, y0=RIM_HEIGHT,
        x1=rim_x_right, y1=RIM_HEIGHT,
        line=dict(color="red", width=3)
    )

    # Add net under the rim (side view)
    net_segments = 6  # number of strands
    net_depth = 1.5   # how far the net hangs down
    net_spacing = RIM_DIAMETER / (net_segments - 1)
    for i in range(net_segments):
        x = rim_x_left + i * net_spacing
        fig.add_shape(
            type="line",
            x0=x, y0=RIM_HEIGHT,
            x1=x, y1=RIM_HEIGHT - net_depth,
            line=dict(color="blue", width=1)  # adjust color/width as needed
        )

    # 3-point line marker (vertical line)
    three_point_distance = BACKBOARD_X + RIM_OFFSET_FROM_BACKBOARD + 19.75
    fig.add_shape(
        type="line",
        x0=three_point_distance, y0=0,
        x1=three_point_distance, y1=16,
        line=dict(color="purple", width=2, dash="dash")
    )
    fig.add_annotation(
        x=three_point_distance, y=16,
        text="3-Point Line",
        showarrow=False,
        yshift=10,
        font=dict(color="purple")
    )

    # Shots (plot real trajectory points)
    for i in selected_idx:
        shot = shots[i]
        color = "green" if shot["result"] == "Make" else "red"
        fig.add_trace(go.Scatter(
            x=shot["side_x"],
            y=shot["side_y"],
            mode="lines+markers",
            line=dict(color=color, width=3),
            marker=dict(size=6),
            name=f"Shot {i+1}"
        ))

    # Layout
    fig.update_layout(
        title="Side View of Ball Trajectory (High-School Court)",
        autosize=True,
        xaxis=dict(range=[HALF_COURT_X + 1, 0],scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[0, 16]),
        height=500
    )

    return to_html(fig, full_html=False)