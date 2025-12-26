import tkinter as tk
from getBusTimes import get_predictions
from datetime import datetime

# ---------- Config ----------
REFRESH_MS = 15000
COLUMN_WIDTH = 220
NUMBER_WIDTH = 3

# Colors
APP_BG = "#f5f5f5"
CARD_BG = "#ffffff"
CARD_BORDER = "#dddddd"

EAST_COLOR = "#1e88e5"
BROWN_COLOR = "#6d4c41"

TEXT_MUTED = "#888888"
DIVIDER = "#eeeeee"

# Fonts
TITLE_FONT = ("Helvetica", 24, "bold")
MIN_FONT = ("Helvetica", 22, "bold")
UNIT_FONT = ("Helvetica", 13)
FOOTER_FONT = ("Helvetica", 11)

# ---------- Root ----------
root = tk.Tk()
root.title("CTA Tracker")
root.configure(bg=APP_BG)

# ---------- Helpers ----------
def minute_color(mins):
    mins = int(mins)
    if mins <= 5:
        return "#d32f2f"
    elif mins <= 10:
        return "#f57c00"
    else:
        return "#2e7d32"

# ---------- Layout ----------
container = tk.Frame(root, bg=APP_BG, padx=40, pady=40)
container.grid()

east_col = tk.Frame(
    container,
    bg=CARD_BG,
    padx=20,
    pady=20,
    highlightbackground=CARD_BORDER,
    highlightthickness=1,
    width=COLUMN_WIDTH
)

brown_col = tk.Frame(
    container,
    bg=CARD_BG,
    padx=20,
    pady=20,
    highlightbackground=CARD_BORDER,
    highlightthickness=1,
    width=COLUMN_WIDTH
)

east_col.grid(row=0, column=0, sticky="n", padx=(0, 20))
brown_col.grid(row=0, column=1, sticky="n")

east_col.grid_propagate(False)
brown_col.grid_propagate(False)

# ---------- Headers ----------
tk.Label(
    east_col,
    text="76 East",
    font=TITLE_FONT,
    fg=EAST_COLOR,
    bg=CARD_BG
).pack(pady=(0, 12))

east_content = tk.Frame(east_col, bg=CARD_BG)
east_content.pack(fill="x")

tk.Label(
    brown_col,
    text="Brown Line",
    font=TITLE_FONT,
    fg=BROWN_COLOR,
    bg=CARD_BG
).pack(pady=(0, 12))

brown_content = tk.Frame(brown_col, bg=CARD_BG)
brown_content.pack(fill="x")

# ---------- Brown Line placeholders ----------
for txt in ("X", "Y"):
    block = tk.Frame(brown_content, bg=CARD_BG)
    block.pack(fill="x", pady=4)

    row = tk.Frame(block, bg=CARD_BG)
    row.pack(fill="x")

    tk.Label(
        row,
        text=txt,
        font=MIN_FONT,
        fg=BROWN_COLOR,
        bg=CARD_BG,
        width=NUMBER_WIDTH,
        anchor="e"
    ).pack(side="left")

    tk.Label(
        row,
        text=" min",
        font=UNIT_FONT,
        fg=TEXT_MUTED,
        bg=CARD_BG
    ).pack(side="left")

    tk.Frame(block, bg=DIVIDER, height=1).pack(fill="x", pady=4)

# ---------- Footer ----------
last_refresh_label = tk.Label(
    container,
    text="Last refresh: --",
    font=FOOTER_FONT,
    fg="#999999",
    bg=APP_BG
)
last_refresh_label.grid(row=1, column=0, columnspan=2, pady=(30, 0))

# ---------- Refresh logic ----------
east_blocks = []

def refresh():
    data = get_predictions()

    for block in east_blocks:
        block.destroy()
    east_blocks.clear()

    if isinstance(data, dict) and "error" in data:
        block = tk.Frame(east_content, bg=CARD_BG)
        block.pack(fill="x", pady=6)

        tk.Label(
            block,
            text="Error loading data",
            font=MIN_FONT,
            fg="#d32f2f",
            bg=CARD_BG
        ).pack()

        east_blocks.append(block)

    else:
        for pred in data:
            number = pred["minutes"].split()[0]

            block = tk.Frame(east_content, bg=CARD_BG)
            block.pack(fill="x", pady=4)

            row = tk.Frame(block, bg=CARD_BG)
            row.pack(fill="x")

            tk.Label(
                row,
                text=number,
                font=MIN_FONT,
                fg=minute_color(number),
                bg=CARD_BG,
                width=NUMBER_WIDTH,
                anchor="e"
            ).pack(side="left")

            tk.Label(
                row,
                text=" min",
                font=UNIT_FONT,
                fg=TEXT_MUTED,
                bg=CARD_BG
            ).pack(side="left")

            tk.Frame(block, bg=DIVIDER, height=1).pack(fill="x", pady=4)

            east_blocks.append(block)

    now = datetime.now().strftime("%I:%M:%S %p")
    last_refresh_label.config(text=f"Last refresh: {now}")

    root.after(REFRESH_MS, refresh)

# ---------- Start ----------
refresh()
root.mainloop()
