import tkinter as tk
import threading
import main
from tkinter import *
from PIL import ImageTk, Image
import customtkinter

# Modes: system (default), light, dark
customtkinter.set_appearance_mode("dark")
# Themes: blue (default), dark-blue, green
customtkinter.set_default_color_theme("dark-blue")

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

text_var = tk.StringVar(value="I.R.I.S.")

# label = customtkinter.CTkLabel(master=root_tk,
#                                textvariable=text_var,
#                                width=120,
#                                height=25,
#                                fg_color=("white", "gray75"),
#                                corner_radius=8)
# label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Create a label to display instructions
# instructions_label = tk.Label(root, text="Click the 'Run' button to start the program.")
instructions_label = customtkinter.CTkLabel(master=root,
                                            textvariable=text_var,
                                            text_color = "darkslategray1",
                                            width=80,
                                            height=25,
                                            fg_color=("#1E1E1E"),
                                            font = ("Georgia",15),
                                            pady = 5,
                                            padx = 2,
                                            corner_radius=8)
instructions_label.pack(pady=6, padx=(4,0), side=tk.BOTTOM, anchor=tk.S)

# Create the "Run" button and attach the function to the command attribute
run_button = customtkinter.CTkButton(root, width=50, corner_radius=8, hover_color="pink", fg_color="transparent",
                                     border_width=3, border_color="purple", text_color="purple", text="Run Iris", command=on_button_click)
run_button.pack(padx=90, pady=(63, 10), side=tk.TOP, anchor=tk.SW)

# Create the "Sleep" button and attach the function to the command attribute
stop_button = customtkinter.CTkButton(root, width=50, corner_radius=8, hover_color="pink", fg_color="transparent",
                                      border_width=3, border_color="purple", text_color="purple", text="Sleep", command=on_stop_button_click)
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
