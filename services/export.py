# Basketball Shot Tracker App
# Developed by Christopher Hong
# Team Name: HoopIQ
# Team Members: Christopher Hong, Alfonso Mejia Vasquez, Gondra Kelly, Matthew Margulies, Carlos Orozco
# Start Web Development Date: October 2025
# Finished Web Development Date: June 2026 (Ideally)
# services/export.py

import csv
from flask import Response
import io

def export_session_csv(shots, session_datetime):
    """
    Export session shot data and component averages to CSV.
    
    shots: list of shot dicts (temporary or from session)
    session_datetime: datetime object of the session
    """

    # Format filename using session date/time
    timestamp_str = session_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"hoopiq_session_{timestamp_str}.csv"

    output = io.StringIO()
    writer = csv.writer(output)

    # 1️⃣ Session date/time
    writer.writerow([f"Session Date & Time: {session_datetime.strftime('%Y-%m-%d %H:%M:%S')}"])
    writer.writerow([])

    # 2️⃣ Shot headers
    shot_headers = ["Shot #", "Backboard", "Rim", "Net Only", "Game Score Point"]
    avg_headers = ["Game Score Point", "Backboard", "Rim", "Net Only", "Backboard & Rim"]
    writer.writerow(shot_headers + [""]*2 + avg_headers)  # header row with spacing

    # 3️⃣ Compute averages
    total_shots = len(shots)
    made_shots = sum(1 for s in shots if s.get("result") == "Make")
    backboard_hits = sum(1 for s in shots if s.get("Backboard"))
    rim_hits = sum(1 for s in shots if s.get("Rim"))
    net_only = sum(1 for s in shots if s.get("Net") and not s.get("Backboard") and not s.get("Rim"))
    backboard_rim_hits = sum(1 for s in shots if s.get("Backboard") and s.get("Rim"))

    fractions = [
    f"'{made_shots}/{total_shots}",
    f"'{backboard_hits}/{total_shots}",
    f"'{rim_hits}/{total_shots}",
    f"'{net_only}/{total_shots}",
    f"'{backboard_rim_hits}/{total_shots}"
]

    percentages = [
        f"{(made_shots/total_shots*100):.1f}%",
        f"{(backboard_hits/total_shots*100):.1f}%",
        f"{(rim_hits/total_shots*100):.1f}%",
        f"{(net_only/total_shots*100):.1f}%",
        f"{(backboard_rim_hits/total_shots*100):.1f}%"
    ]

    # 4️⃣ Build rows: align fraction & percentage with top shot row
    max_rows = max(len(shots), 2)  # 2 rows for fraction and percentage
    for i in range(max_rows):
        # Shot data
        if i < len(shots):
            shot = shots[i]
            shot_row = [
                i+1,
                1 if shot.get("Backboard") else 0,
                1 if shot.get("Rim") else 0,
                1 if shot.get("Net") and not shot.get("Backboard") and not shot.get("Rim") else 0,
                1 if shot.get("result") == "Make" else 0
            ]
        else:
            shot_row = [""]*len(shot_headers)

        # Spacing
        shot_row += ["", ""]

        # Average columns
        if i == 0:
            avg_row = fractions
        elif i == 1:
            avg_row = percentages
        else:
            avg_row = [""]*len(avg_headers)

        writer.writerow(shot_row + avg_row)

    # Build response
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )