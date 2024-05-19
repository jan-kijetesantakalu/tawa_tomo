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


# Adding temp images
lava = Image.open('assets/lavaLamp.jpg').resize((int(WIDTH/10), int(HEIGHT/10)))
lava = ImageTk.PhotoImage(lava)
tk.Label(root, image = lava).place(x = int(WIDTH/4*1.35),y = (int(HEIGHT/2*0.9)))

lamp = Image.open('assets/lamp.jpg').resize((int(WIDTH/10), int(HEIGHT/10)))
lamp = ImageTk.PhotoImage(lamp)
tk.Label(root, image = lamp).place(x = int(WIDTH/3*1.8),y = (int(HEIGHT/2*0.9)))

ort = Image.open('assets/Ort.jpg').resize((int(WIDTH/10), int(HEIGHT/10)))
ort = ImageTk.PhotoImage(ort)
tk.Label(root, image = ort).place(x = int(WIDTH/4*2.5),y = (int(HEIGHT/2*1.4)))


# checks 2 rules against each other, returns TRUE if they don't contradict
def rule_compatability(rule1, rule2):
    if rule1 == rule2:
        return False

    #If asking for same type of thing in same room
    if rule1["room_top"] == rule2["room_top"] and rule1["room_top"] != None and rule1["type"] == rule2["type"] and rule1["type"] != None:
        return False

    return True

 

#make rules for objects
rules = []
num_rules = 6

type_options = types*2

class VarietyException(Exception):
    pass

while len(rules) < num_rules:
    try:
        obj_variety = 192
        pos_variety = 12
        target = 24
    
        rule = {"obj": True, "room_top": None, "room_left": None, "type": None, "colour": None, "style": None}
    
        rule["room_top"] = choice([True, False, None])
        if rule["room_top"] != None:
            obj_variety /= 2
            pos_variety /=2
            if obj_variety * pos_variety <= target:
                raise(VarietyException)

        rule["room_left"] = choice([True, False, None])
        if rule["room_left"] != None:
            obj_variety /= 2
            pos_variety /= 2
            if obj_variety * pos_variety <= target: 
                raise(VarietyException) 

        if choice([True, True, None]):
            rule["type"] = type_options.pop(type_options.index(choice(type_options)))
        else:
            rule["type"] = None
        
        if rule["type"] != None:
            obj_variety /= 3
            pos_variety /= 3
            if obj_variety * pos_variety <= target:    
                raise(VarietyException)

        rule["colour"] = choice(colours+([None]))
        if rule["colour"] != None:
            obj_variety /= 4
            if obj_variety * pos_variety <= target:
                raise(VarietyException) 

        rule["style"] = choice(styles+([None]))
        if rule["style"] != None:
            obj_variety /= 4
            if obj_variety * pos_variety <= target:
                raise(VarietyException)

        raise(VarietyException)

    except VarietyException:
        comp = True
        for rul in rules:
            if not comp:
                break
            else:
                comp = rule_compatability(rule, rul)
        if comp:
            rules.append(rule)   
        elif rule["type"] != None:
            type_options.append(rule["type"])



# make rules for room colour
walls = []
num_wall_rules = 4
wall_option_top = [True, True, False, False]
wall_option_left = [True, True, False, False]

while len(walls) < num_wall_rules:
    wall = {"obj": False, "top": None, "left": None, "colour": None}
    valid = True

    if choice([True, True, False]):
        # choose option from list for wall option top and remove it
        wall["top"] = wall_option_top.pop(wall_option_top.index(choice(wall_option_top)))
    else:
        # set to None 1/3 of the time
        wall["top"] = None
    

    if choice([True, True, False]):
        # choose option from list for wall option top and remove it
        wall["left"] = wall_option_left.pop(wall_option_left.index(choice(wall_option_left)))
    else:
        # set to None 1/3 of the time
        wall["left"] = None

    wall["colour"] = choice(colours)
    
    for wal in walls:
        if wall["top"] == wal["top"] and wal["top"] != None and wall["left"] == wal["left"] and wal["left"] != None:
            valid = False
        
        if wal == wall:
            valid = False

    if not valid:
        wall_option_top.append(wal["top"])
        wall_option_left.append(wal["left"])
        continue
    else: 
        walls.append(wall)

rules += walls

for rule in rules:
    print(rule)

#Mainloop
root.mainloop()
