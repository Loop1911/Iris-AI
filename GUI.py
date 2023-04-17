import tkinter as tk
import threading
import main

# Define a function to run when the "Run" button is clicked
def on_button_click():
    global running_thread
    # If the code is already running, do nothing
    if running_thread and running_thread.is_alive():
        return
    # Otherwise, start a new thread to run the code
    running_thread = threading.Thread(target=main.everything_function)
    running_thread.start()

# Define a function to run when the "Stop" button is clicked
def on_stop_button_click():
    global running_thread
    # If the code is currently running, set the stop flag to gracefully exit the thread
    if running_thread and running_thread.is_alive():
        main.stop_flag = False

# Create the root window
root = tk.Tk()
root.title("Iris GUI")
root.geometry("300x300")

# Create a label to display instructions
instructions_label = tk.Label(root, text="Click the 'Run' button to start the program.")
instructions_label.pack(pady=10)

# Create the "Run" button and attach the function to the command attribute
run_button = tk.Button(root, text="Run Iris", command=on_button_click)
run_button.pack(pady=5)

# Create the "Stop" button and attach the function to the command attribute
stop_button = tk.Button(root, text="Stop", command=on_stop_button_click)
stop_button.pack(pady=5)

# Create a global variable to track the running thread
running_thread = None

# Start the event loop
root.mainloop()
