import tkinter as tk
import threading
import main
from tkinter import *
from PIL import ImageTk, Image

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
root.geometry("300x250")

# Open the image file
bg_image = Image.open("assets/background.jpg")

# Resize the image to fit the window size
resized_bg_image = bg_image.resize((300, 250), Image.LANCZOS)

# Convert the image to a PhotoImage object
tk_bg_image = ImageTk.PhotoImage(resized_bg_image)

# Create a Label widget with the image
bg_label = Label(root, image=tk_bg_image)
bg_label.place(x=0, y=0)

# Create a label to display instructions
instructions_label = tk.Label(root, text="Click the 'Run' button to start the program.")
instructions_label.pack(pady=10, side=tk.BOTTOM, anchor=tk.S)

# Create the "Run" button and attach the function to the command attribute
run_button = tk.Button(root, text="Run Iris", command=on_button_click)
run_button.pack(padx=90, pady=(63,10), side=tk.TOP, anchor=tk.SW)

# Create the "Sleep" button and attach the function to the command attribute
stop_button = tk.Button(root, text="Sleep", command=on_stop_button_click)
stop_button.pack(padx=95, side=tk.LEFT, anchor=tk.N)

# Create a global variable to track the running thread
running_thread = None

# Start the event loop
root.mainloop()


# from tkinter import *
# from PIL import ImageTk, Image

# root = Tk()
# root.geometry("500x500")

# # Open the image file
# bg_image = Image.open("background.png")

# # Resize the image to fit the window size
# resized_bg_image = bg_image.resize((500, 500), Image.ANTIALIAS)

# # Convert the image to a PhotoImage object
# tk_bg_image = ImageTk.PhotoImage(resized_bg_image)

# # Create a Label widget with the image
# bg_label = Label(root, image=tk_bg_image)
# bg_label.place(x=0, y=0)

# # Add other widgets to the window as needed

# root.mainloop()