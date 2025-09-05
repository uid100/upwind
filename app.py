#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: app.py

from flask import Flask, render_template, request
import io
import base64
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)

def hours_to_hms(hours):
    if hours == float("inf"):
        return "∞"
    total_seconds = int(hours * 3600)
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def make_bent_line(angle_deg, final_y):
    angle_rad = np.radians(angle_deg)
    half_y = final_y / 2
    seg_len = half_y / np.cos(angle_rad) if np.cos(angle_rad) != 0 else float("inf")

    x0, y0 = 0, 0
    x1 = x0 + seg_len * np.sin(angle_rad)
    y1 = y0 + seg_len * np.cos(angle_rad)

    angle_rad2 = -angle_rad
    x2 = x1 + seg_len * np.sin(angle_rad2)
    y2 = y1 + seg_len * np.cos(angle_rad2)

    xs = [x0, x1, x2]
    ys = [y0, y1, y2]
    return np.array(xs), np.array(ys), seg_len

@app.route("/", methods=["GET", "POST"])
def index():
    # Endpoint distance (final Y)
    distance = float(request.form.get("distance", 1.0))
    # Units
    units = request.form.get("units", "miles")
    speed_units = request.form.get("speed_units", "knots")
    length_units = request.form.get("length_units", "ft")
    # Boat inputs
    speed_a = float(request.form.get("speed_a", 4.0))
    angle_a = float(request.form.get("angle_a", 40))
    length_a = float(request.form.get("length_a", 20.0))
    speed_b = float(request.form.get("speed_b", 5.0))
    angle_b = float(request.form.get("angle_b", 50))
    length_b = float(request.form.get("length_b", 20.0))
    # Lengths/sec
    lengths_per_sec_a = speed_a / length_a
    lengths_per_sec_b = speed_b / length_b

    # Bent lines
    xs_a, ys_a, seg_len_a = make_bent_line(angle_a, distance)
    xs_b, ys_b, seg_len_b = make_bent_line(angle_b, distance)
    total_len_a = 2 * seg_len_a
    total_len_b = 2 * seg_len_b

    # Times
    time_a1 = seg_len_a / speed_a if speed_a > 0 else float("inf")
    total_time_a = 2 * time_a1
    time_b1 = seg_len_b / speed_b if speed_b > 0 else float("inf")
    total_time_b = 2 * time_b1

    # Annotation offsets
    if total_time_a < total_time_b:
        y_offset_a_half = 15
        y_offset_a_end  = 15
        y_offset_b_half = -15
        y_offset_b_end  = -15
    else:
        y_offset_a_half = -15
        y_offset_a_end  = -15
        y_offset_b_half = 15
        y_offset_b_end  = 15

    # Plot
    fig, ax = plt.subplots()
    ax.plot(xs_a, ys_a, marker="o",
            label=f"Boat A: {total_len_a:.2f} {units}, {hours_to_hms(total_time_a)} @ {speed_a:.1f} {speed_units}")
    ax.plot(xs_b, ys_b, marker="o",
            label=f"Boat B: {total_len_b:.2f} {units}, {hours_to_hms(total_time_b)} @ {speed_b:.1f} {speed_units}")

    # Annotate halfway & endpoint times
    ax.annotate(hours_to_hms(time_a1), (xs_a[1], ys_a[1]), textcoords="offset points", xytext=(10,y_offset_a_half))
    ax.annotate(hours_to_hms(total_time_a), (xs_a[2], ys_a[2]), textcoords="offset points", xytext=(10,y_offset_a_end))
    ax.annotate(hours_to_hms(time_b1), (xs_b[1], ys_b[1]), textcoords="offset points", xytext=(10,y_offset_b_half))
    ax.annotate(hours_to_hms(total_time_b), (xs_b[2], ys_b[2]), textcoords="offset points", xytext=(10,y_offset_b_end))

    # Time & distance difference
    time_diff_sec = abs(total_time_a - total_time_b) * 3600
    max_boat_length = max(length_a, length_b)
    dist_diff_lengths = abs(total_len_a - total_len_b) / max_boat_length
    diff_label = f"ΔTime: {time_diff_sec:.1f} s, ΔDistance: {dist_diff_lengths:.2f} boat lengths"
    ax.plot([], [], ' ', label=diff_label)  # invisible line for legend

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()
    ax.grid(True)
    ax.set_aspect("equal", adjustable="datalim")

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plot_data = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)

    return render_template(
        "index.html",
        plot_url=plot_data,
        distance=distance,
        units=units,
        speed_units=speed_units,
        length_units=length_units,
        speed_a=speed_a,
        angle_a=angle_a,
        length_a=length_a,
        speed_b=speed_b,
        angle_b=angle_b,
        length_b=length_b,
        lengths_per_sec_a=lengths_per_sec_a,
        lengths_per_sec_b=lengths_per_sec_b
    )

if __name__ == "__main__":
    # app.run(debug=True, host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port=5000)
