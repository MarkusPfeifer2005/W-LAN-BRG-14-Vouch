import tkinter as tk
from tkinter import messagebox
import PIL  # If you haven't already, please install this library, it is very useful anyway.
from PIL import ImageTk, Image

# Initializes a window.
root = tk.Tk()
root.geometry("150x200")
frame1 = tk.Frame(root)
frame1.pack()


# Calls a Info-window.
def get_info():
    messagebox.showinfo("Info!", "You pressed a button!")


# Creates Button containing simple text.
button1 = tk.Button(frame1, text="press this button", command=get_info)
button1.pack()
# Creates button made from image.
image1 = tk.PhotoImage(file="billo_button.png")
button2 = tk.Button(frame1, image=image1, command=get_info, borderwidth=0)
button2.pack()
# another too big button
image2 = tk.PhotoImage(file="billo_button-large.png")
button3 = tk.Button(frame1, image=image2, command=get_info, borderwidth=0)
button3.pack()


root.mainloop()  # updates the window

# Task:
# Please find a way to make the large(red) button roughly as small as the small(blue) button.
