global WIDTH, HEIGHT, SCALE, colours, styles

types = ["lamp", "hanging", "tat"]
colours = ["red", "blue", "green", "yellow"]
styles = ["modern", "antique", "retro", "unusual"]

import tkinter as tk
from random import *
from PIL import Image, ImageTk

#Room definition (const)
rooms = {"kitchen": {}, "bedroom": {}, "bathroom":{}, "lounge": {}} #Contains the rooms
rooms["kitchen"]  = {"colour": choice(colours), 
                     "hanging": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None}, 
                     "lamp": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None},
                     "tat": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None},
                    "top": False,
                    "left": False,
                    "img": None,
                    "label": None,
                     "xpos": None,
                     "ypos": None
                    }
rooms["bedroom"]  = {"colour": choice(colours), 
                     "hanging": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None}, 
                     "lamp": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None},
                     "tat": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None},
                    "top": True,
                    "left": False,
                    "img": None,
                    "label": None,
                     "xpos": None,
                     "ypos": None

                    }
rooms["bathroom"]  = {"colour": choice(colours), 
                     "hanging": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None}, 
                     "lamp": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None},
                      "tat": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None},
                    "top": True,
                    "left": True,
                    "img": None,
                    "label": None,
                     "xpos": None,
                     "ypos": None

                    }
rooms["lounge"]  = {"colour": choice(colours), 
                     "hanging": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None}, 
                     "lamp": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None},
                    "tat": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None},
                    "top": False,
                    "left": True,
                    "img": None,
                    "label": None,
                     "xpos": None,
                     "ypos": None
                    
                    }


#Create Root Window
root = tk.Tk()
root.attributes('-fullscreen', True)
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
SCALE = HEIGHT/ (512+160) #Scale factor for objects, for rooms and house it is 2x


#Load and Place Background
try:
    house_img = Image.open('assets/house.png') # If house.png does not open -
except FileNotFoundError:
    print(f'''Failed opening: assets/house.png''')
    house_img = Image.open('assets/house_placeholder.png') # - Use placeholder
    
house_img = house_img.resize((int(768*SCALE), int(512*SCALE)))

house_img = ImageTk.PhotoImage(house_img)
house = tk.Label(root, image = house_img).place(x=int((WIDTH-(768*SCALE))/2), y=int(HEIGHT-(512*SCALE)))


def create_object(room, rooms, obj_type):
    try:
        rooms[room][obj_type]["img"] = Image.open(f'''assets/{room}/{obj_type}/{rooms[room][obj_type]["style"]}/{room}_{rooms[room][obj_type]["style"]}_{rooms[room][obj_type]["colour"]}_{obj_type}.png''')
    except FileNotFoundError:
        print(f'''Failed opening: assets/{room}/{obj_type}/{rooms[room][obj_type]["style"]}/{room}_{rooms[room][obj_type]["style"]}_{rooms[room][obj_type]["colour"]}_{obj_type}.png''')
        rooms[room][obj_type]["img"] = Image.open(f'''assets/placeholder.png''')
    
    rooms[room][obj_type]["img"] = rooms[room][obj_type]["img"].resize((int(32*SCALE), int(32*SCALE)))

    rooms[room][obj_type]["img"] = ImageTk.PhotoImage(rooms[room][obj_type]["img"])
    rooms[room][obj_type]["label"] = tk.Label(root, image = rooms[room][obj_type]["img"]) 
    rooms[room][obj_type]["label"].place(x = rooms[room]["xpos"], y = rooms[room]["ypos"])
    

def create_rooms(rooms):
    for room in rooms.keys():
        try:
            rooms[room]["img"]= Image.open(f'''assets/{room}/room/{room}_{rooms[room]["colour"]}.png''')
        except FileNotFoundError:
            print(f'''Failed opening: assets/{room}/room/{room}_{rooms[room]["colour"]}.png''')

            rooms[room]["img"] = Image.open(f'''assets/room_placeholder.png''')

        rooms[room]["img"] = rooms[room]["img"].resize((int(384*SCALE), int(256*SCALE)))
        
        rooms[room]["img"] =  ImageTk.PhotoImage(rooms[room]["img"])
        
        xpos = int((WIDTH-(768*SCALE))/2)
        if not rooms[room]["left"]:
            xpos += 384*SCALE

        ypos = int(HEIGHT-(512*SCALE))
        if not rooms[room]["top"]:
            ypos += 256*SCALE

        rooms[room]["label"] = tk.Label(root, image = rooms[room]["img"])
        rooms[room]["label"].place(x = xpos, y = ypos)

        rooms[room]["xpos"] = xpos
        rooms[room]["ypos"] = ypos

        for obj in ["hanging", "lamp", "tat"]:
            create_object(room, rooms, obj)

create_rooms(rooms)

#Place Quit Button
quit = tk.Button(root, text="QUIT", bg="darkred", fg = "white", command=root.destroy)
quit.place(x = 0, y = 0) #Ugly and Hardcoded, fix later

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
