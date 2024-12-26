import time
import os
import tkinter as tk
import threading
from pynput.mouse import Listener
from pynput.keyboard import Listener as KeyboardListener

INACTIVITY_LIMIT = 60 * 60 * 2
COUNTDOWN_TIME = 60  

last_active_time = time.time() 
window = None  
countdown_running = False  

def on_move(x, y):
    global last_active_time
    last_active_time = time.time()

def on_press(key):
    global last_active_time
    last_active_time = time.time()

def show_countdown(seconds):
    global window
    if window is None:
        window = tk.Tk()
        window.attributes('-fullscreen', True)  
        window.configure(bg='black')
        window.protocol("WM_DELETE_WINDOW", exit_program)
        window.attributes('-topmost', True)  
        window.geometry("1920x1080")  
        window.title("Shutdown Countdown")

   
    for widget in window.winfo_children():
        widget.destroy()

   
    label = tk.Label(window, text=f"Shutting down in {seconds} seconds", font=("Arial", 50), fg="white", bg="black")
    label.pack(expand=True)

  
    progress_bar = tk.Canvas(window, width=500, height=50, bg="black", bd=0, highlightthickness=0)
    progress_bar.pack(expand=True)

   
    progress_bar.create_rectangle(0, 0, 500, 50, fill="gray")

    
    progress = 500 * (seconds / COUNTDOWN_TIME)
    progress_bar.create_rectangle(0, 0, progress, 50, fill="green")

    window.deiconify()  
    window.update_idletasks()  
    window.after(100, lambda: window.lift())  

def check_inactivity():
    global last_active_time, countdown_running
    while True:
        time.sleep(1)
        if time.time() - last_active_time > INACTIVITY_LIMIT and not countdown_running:
            countdown_running = True
            countdown()

def countdown():
    global countdown_running
    for i in range(COUNTDOWN_TIME, -1, -1):  
        show_countdown(i)
        time.sleep(1)
        if time.time() - last_active_time <= INACTIVITY_LIMIT:  
            countdown_running = False  
            window.withdraw()  
            return  

    print("Shutting down the system")  
    os.system("shutdown /s /t 1")  

def exit_program():
    global window
    if window:
        window.quit()
    exit()

def start_program():
    inactivity_thread = threading.Thread(target=check_inactivity, daemon=True)
    inactivity_thread.start()

    mouse_listener = Listener(on_move=on_move)
    keyboard_listener = KeyboardListener(on_press=on_press)
    
    mouse_listener.start()
    keyboard_listener.start()

    mouse_listener.join()
    keyboard_listener.join()

if __name__ == "__main__":
    start_program()
