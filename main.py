global WIDTH, HEIGHT

import tkinter as tk
from PIL import Image, ImageTk

#Create Root Window
root = tk.Tk()
root.attributes('-fullscreen', True)
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()


#Load and Place Background
img = Image.open('assets/back.jpg').resize((WIDTH, HEIGHT)) #TEMP Image (When real image is used white borders [should] disappear)
img = ImageTk.PhotoImage(img)
tk.Label(root, image = img).place(x=0, y=0)

#Place Quit Button
quit = tk.Button(root, text="QUIT", bg="darkred", fg = "white", command=root.destroy)
quit.place(x=WIDTH-35,y=0) #Ugly and Hardcoded, fix later

#Mainloop
root.mainloop()
