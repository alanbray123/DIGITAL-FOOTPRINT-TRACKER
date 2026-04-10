import customtkinter as ctk
from dist.database import fetch_logs

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("900x650")
app.title("Digital Tracker")

# ===== COLORS =====
GREEN = "#00ff9c"
YELLOW = "#ffd000"
RED = "#ff3b3b"
CARD = "#1a1a1a"

# ===== TITLE =====
title = ctk.CTkLabel(
    app,
    text="Digital Footprint Tracker",
    font=("Segoe UI", 26, "bold"),
    text_color=GREEN
)
title.pack(pady=15)

# ===== CURRENT APP =====
current_label = ctk.CTkLabel(
    app,
    text="Now Using: ...",
    font=("Segoe UI", 16),
    text_color=YELLOW
)
current_label.pack(pady=5)

# ===== SCROLL AREA =====
scroll = ctk.CTkScrollableFrame(app)
scroll.pack(fill="both", expand=True, padx=20, pady=10)

# ===== SUMMARY =====
summary = ctk.CTkFrame(scroll, fg_color=CARD, corner_radius=15)
summary.pack(fill="x", pady=10)

total_label = ctk.CTkLabel(summary, text="Today: 0 min", font=("Segoe UI", 18))
total_label.pack(anchor="w", padx=20, pady=5)

top_label = ctk.CTkLabel(summary, text="Top App: -", font=("Segoe UI", 18))
top_label.pack(anchor="w", padx=20, pady=5)

# ===== COLOR LOGIC =====
def get_color(minutes):
    if minutes < 1:
        return GREEN
    elif minutes < 5:
        return YELLOW
    else:
        return RED

# ===== PARSE FUNCTION =====
def parse_activity(activity):
    parts = activity.split("|")
    if len(parts) >= 2:
        return parts[0].strip(), parts[-1].strip()
    return None, None

# ===== LOAD DATA =====
def load_data():
    logs = fetch_logs()

    # clear old cards (keep summary)
    for widget in scroll.winfo_children():
        if widget != summary:
            widget.destroy()

    app_usage = {}
    total_time = 0

    for log in logs:
        if "|" in log[1]:
            try:
                name, time = parse_activity(log[1])
                if not name or not time:
                    continue

                seconds = float(time.replace("sec", "").strip())

                app_usage[name] = app_usage.get(name, 0) + seconds
                total_time += seconds
            except:
                pass

    # ===== CURRENT APP =====
    if logs:
        name, _ = parse_activity(logs[-1][1])
        if name:
            current_label.configure(text=f"Now Using: {name}")

    # ===== SUMMARY =====
    if app_usage:
        top_app = max(app_usage, key=app_usage.get)
    else:
        top_app = "-"

    total_label.configure(text=f"Today: {round(total_time/60, 2)} min")
    top_label.configure(text=f"Top App: {top_app}")

    max_time = max(app_usage.values()) if app_usage else 1

    # ===== CARDS =====
    for app_name, seconds in sorted(app_usage.items(), key=lambda x: x[1], reverse=True):
        minutes = seconds / 60
        percent = min(seconds / max_time, 1)

        color = get_color(minutes)

        card = ctk.CTkFrame(scroll, fg_color=CARD, corner_radius=15)
        card.pack(fill="x", pady=8, padx=5)

        name_label = ctk.CTkLabel(
            card,
            text=app_name[:40],
            font=("Segoe UI", 18, "bold")
        )
        name_label.pack(anchor="w", padx=15, pady=(8, 0))

        time_label = ctk.CTkLabel(
            card,
            text=f"{round(minutes,2)} min",
            text_color=color,
            font=("Segoe UI", 14)
        )
        time_label.pack(anchor="w", padx=15)

        # ===== PROGRESS BAR =====
        bar_bg = ctk.CTkFrame(card, height=10, fg_color="#2a2a2a", corner_radius=8)
        bar_bg.pack(fill="x", padx=15, pady=10)

        bar = ctk.CTkFrame(
            bar_bg,
            height=10,
            width=int(percent * 500),
            fg_color=color,
            corner_radius=8
        )
        bar.pack(side="left")

# ===== AUTO REFRESH =====
def auto_refresh():
    load_data()
    app.after(4000, auto_refresh)

auto_refresh()

app.mainloop()