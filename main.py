from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
# Define color codes and font for the UI
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# Time durations in minutes
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# Initialize repetition counter and timer ID
reps = 1
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    """
    Resets the timer, UI labels, and repetition counter.
    Cancels any running countdown.
    """
    global reps, timer
    window.after_cancel(timer)  # Cancel scheduled after() calls
    reps = 1  # Reset repetition counter
    canvas.itemconfig(timer_text, text="00:00")  # Reset timer display
    timer_label.config(text="Timer", fg=GREEN)  # Reset label to default
    check_mark_label.config(text="")  # Clear check marks


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    """
    Starts the timer depending on the current repetition count.
    Alternates between work, short break, and long break sessions.
    """
    global reps
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # Work sessions on odd reps
    if reps in [1, 3, 5, 7]:
        countdown(work_sec)
        timer_label.config(text="Work", fg=GREEN)
        reps += 1
    # Short breaks on even reps
    elif reps in [2, 4, 6]:
        countdown(short_break_sec)
        timer_label.config(text="Break", fg=PINK)
        reps += 1
    # Long break on the 8th rep
    elif reps == 8:
        countdown(long_break_sec)
        timer_label.config(text="Break", fg=RED)
        reps += 1


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(count):
    """
    Updates the timer every second using window.after().
    When timer reaches zero, it automatically starts the next session.
    Displays completed work session check marks.
    """
    global timer
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    # Update timer text on the canvas
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        # Schedule the function to run after 1 second
        timer = window.after(1000, countdown, count - 1)
    else:
        # Automatically start the next session
        start_timer()
        # Calculate completed work sessions and update check marks
        marks = ""
        work_sessions = math.floor((reps - 1) / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_mark_label.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
# Create the main window
window = Tk()
window.title("Pomodoro")
window.configure(padx=100, pady=50, bg=YELLOW)

# Set up canvas with tomato image and timer text
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.pack()

# Timer label (top of the window)
timer_label = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 40), bg=YELLOW)
timer_label.place(relx=0.5, y=-30, anchor=CENTER)

# Label for displaying check marks (bottom of the window)
check_mark_label = Label(text="", fg=GREEN, bg=YELLOW)
check_mark_label.place(relx=0.5, y=250, anchor=CENTER)

# Start button to initiate the timer
start_button = Button(text="Start", command=start_timer, highlightbackground=YELLOW)
start_button.place(x=-50, y=240)

# Reset button to stop and clear the timer
reset_button = Button(text="Reset", command=reset_timer, highlightbackground=YELLOW)
reset_button.place(x=150, y=240)

# Start the GUI event loop
window.mainloop()







