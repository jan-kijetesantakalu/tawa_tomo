global WIDTH, HEIGHT, colours, styles

types = ["lamp", "hanging", "tat"]
colours = ["red", "blue", "green", "yellow"]
styles = ["modern", "antique", "retro", "unusual"]

import tkinter as tk
from random import *
from PIL import Image, ImageTk

#Room definition (const)
rooms = {"kitchen": {}, "bedroom": {}, "bathroom":{}, "lounge": {}} #Contains the rooms
rooms["kitchen"]  = {"colour": choice(colours), 
                    "hanging": {"colour": choice(colours), "style": choice(styles)}, 
                    "lamp": {"colour": choice(colours), "style": choice(styles)},
                    "tat": {"colour": choice(colours), "style": choice(styles)},
                    "top": False,
                    "left": False
                    }
rooms["bedroom"]  = {"colour": choice(colours), 
                    "hanging": {"colour": choice(colours), "style": choice(styles)}, 
                    "lamp": {"colour": choice(colours), "style": choice(styles)},
                    "tat": {"colour": choice(colours), "style": choice(styles)},
                    "top": True,
                    "left": False
                    }
rooms["bathroom"]  = {"colour": choice(colours), 
                    "hanging": {"colour": choice(colours), "style": choice(styles)}, 
                    "lamp": {"colour": choice(colours), "style": choice(styles)},
                    "tat": {"colour": choice(colours), "style": choice(styles)},
                    "top": True,
                    "left": True 
                    }
rooms["lounge"]  = {"colour": choice(colours), 
                    "hanging": {"colour": choice(colours), "style": choice(styles)}, 
                    "lamp": {"colour": choice(colours), "style": choice(styles)},
                    "tat": {"colour": choice(colours), "style": choice(styles)},
                    "top": False,
                    "left": True
                    }


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
quit.place(x = int(WIDTH/2), y = 0) #Ugly and Hardcoded, fix later


# Adding stoof
lava = Image.open('assets/lavaLamp.jpg').resize((int(WIDTH/10), int(HEIGHT/10)))
lava = ImageTk.PhotoImage(lava)
tk.Label(root, image = lava).place(x = int(WIDTH/4*1.35),y = (int(HEIGHT/2*0.9)))

lamp = Image.open('assets/lamp.jpg').resize((int(WIDTH/10), int(HEIGHT/10)))
lamp = ImageTk.PhotoImage(lamp)
tk.Label(root, image = lamp).place(x = int(WIDTH/3*1.8),y = (int(HEIGHT/2*0.9)))

ort = Image.open('assets/Ort.jpg').resize((int(WIDTH/10), int(HEIGHT/10)))
ort = ImageTk.PhotoImage(ort)
tk.Label(root, image = ort).place(x = int(WIDTH/4*2.5),y = (int(HEIGHT/2*1.4)))


#Rules
"""
objectrule : {
    obj = true
	n : int
	strict : bool
	room_top : bool
	room_left : bool
	type : str | any
	style : str | any
	colour : str | any
	
}

roomrule : {
    obj = false
	n : int
	strict : bool
	top : bool  | any
	left : bool | any
	colour : str (red/yellow/blue/green/warm/cold)
}
"""
    
rules = []
rule = {}
rule["room_top"] = choice([True, False, None])
rule["room_left"] = choice([True, False, None])
rule["type"] = choice(types+([None]*4))



rule["colour"] = choice(colours+([None]*4))
rule["style"] = choice(styles+([None]*4))



print(rules)    


#Mainloop
root.mainloop()
