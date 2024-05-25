global WIDTH, HEIGHT, colours, styles, types, canvas, canvas_label, canvas_tk, cursor_pos, cursor_order, redraw, mainloop, to_do, to_do_pos, to_do_after_id, update_to_do, sleep_pos, sleep_after_idi, sleep_frames #, SCALE


import tkinter as tk
from random import *
from PIL import Image, ImageTk, ImageDraw
from math import floor
import glob


redraw = True
mainloop = True
types   = ["lamp", "hanging", "tat"]
colours = ["red", "blue", "green", "yellow"]
styles  = ["modern", "antique", "retro", "unusual"]
cursor_pos = 0
to_do_pos = 1
cursor_order = [("bathroom", "wall"), ("bathroom", "hanging"), ("bathroom", "tat"), ("bathroom", "lamp"), 
                ("bedroom", "wall"), ("bedroom", "tat"), ("bedroom", "lamp"), ("bedroom", "hanging"),
                ("lounge", "wall"), ("lounge", "tat"), ("lounge", "hanging"), ("lounge", "lamp"),
                ("kitchen", "wall"), ("kitchen", "lamp"), ("kitchen", "hanging"), ("kitchen", "tat")]
to_do = Image.open("assets/to_do.png")
update_to_do = True
sleep_pos = 0
sleep_frames = 0


#Initial Room Definition

rooms = {"kitchen": {}, "bedroom": {}, "bathroom":{}, "lounge": {}} #Contains the rooms

rooms["kitchen"]  = {
        "colour": choice(colours), 
                     
        "hanging": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 71, "ypos": 59}, 
        "lamp": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 39, "ypos": 86},
        "tat": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 143, "ypos": 86},
                    
        "top": False,
        "left": False,
                    
        "img": None,
        "xpos": None,
        "ypos": None
}

rooms["bedroom"]  = {
       "colour": choice(colours), 
        
        "hanging": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 171, "ypos": 67}, 
        "lamp": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 115, "ypos": 107},
        "tat": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 77, "ypos": 95},
                    
        "top": True,
        "left": False,
                    
        "img": None,
        "xpos": None,
        "ypos": None
}

rooms["bathroom"]  = {
        "colour": choice(colours), 
                    
        "hanging": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos":51, "ypos":95}, 
        "lamp": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos":183, "ypos":67},
        "tat": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos":103, "ypos":123},
        
        "top": True,
        "left": True,
                    
        "img": None,
        "xpos": None,
        "ypos": None
}

rooms["lounge"]  = {
        "colour": choice(colours), 
        
        "hanging": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 139, "ypos": 63}, 
        "lamp": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 183, "ypos": 123},
        "tat": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 87, "ypos": 123},
                    
        "top": False,
        "left": True,
                    
        "img": None,
        "xpos": None,
        "ypos": None            
}
root = tk.Tk()

def destroy_window():
    global mainloop
    mainloop = False

#Create Root Window
root.attributes('-fullscreen', True)
root.protocol("WM_DELETE_WINDOW", destroy_window)

def cursor_next(e):
    global cursor_pos, redraw
    cursor_pos += 1
    cursor_pos %= 16
    redraw = True

def cursor_prev(e):
    global cursor_pos, redraw
    cursor_pos -= 1
    cursor_pos %= 16
    redraw = True

def hide_to_do(e=None):
    global redraw, to_do_pos, to_do_after_id    
    redraw = True   
    
    if to_do_pos > 0.01:    
        to_do_pos -= 0.01+(to_do_pos/12)+(to_do_pos/4)**1.5
        try:
            root.after_cancel(to_do_after_id)
        except NameError:
            # if event not defined
            pass
        to_do_after_id = root.after(1, hide_to_do)
    to_do_pos = max(to_do_pos, 0)



def show_to_do(e=None):
    global redraw, to_do_pos, to_do_after_id    
    redraw = True
    
    if to_do_pos < 0.99:
        to_do_pos += 0.01+((1-to_do_pos)/12)+((1-to_do_pos)/4)**1.5
        try:
            root.after_cancel(to_do_after_id)
        except NameError:
            # if event not defined
            pass
        to_do_after_id = root.after(1, show_to_do)
    to_do_pos = min(to_do_pos, 1)
   

def hide_sleep(e=None):
    global redraw, sleep_pos, sleep_after_id
    redraw = True

    if sleep_pos > 0:
        sleep_pos -= 0.03+(sleep_pos/16)+(sleep_pos/4)**2
        try:
            root.after_cancel(sleep_after_id)
        except NameError:
            # if event not defined
            pass
        sleep_after_id = root.after(1, hide_sleep)
    sleep_pos = max(sleep_pos, 0)


def show_sleep(e=None):
    global redraw, sleep_pos, sleep_after_id
    redraw = True
    hide_to_do()

    if sleep_pos < 1:
        sleep_pos += 0.03+((1-sleep_pos)/16)+((1-sleep_pos)/4)**2
        try:
            root.after_cancel(sleep_after_id)
        except NameError:
            # if event not defined
            pass
        sleep_after_id = root.after(1, show_sleep)
    sleep_pos = min(sleep_pos, 1)


def commit_sleep():
    global redraw, update_to_do, sleep_frames
#    hide_sleep()
    redraw = True
    sleep_frames = 100    
#    update_to_do = True
#    show_to_do()
    

def handle_keypress(e):
    global cursor_pos, redraw
    
    cursor_loc = cursor_order[cursor_pos]
    cursor_room = rooms[cursor_loc[0]]
    cursor_obj = cursor_room[cursor_loc[1]] if cursor_loc[1] != "wall" else cursor_room
    
    if e.char.lower() == "q":
        if sleep_pos > 0.75:
            commit_sleep()
        else:
            show_sleep()

    elif e.char.lower() == "w":
        hide_sleep()


    elif e.char.lower() == "a":
        cursor_obj["colour"] = "red"
    
    elif e.char.lower() == "s":
        cursor_obj["colour"] = "yellow"
    
    elif e.char.lower() == "d":
        cursor_obj["colour"] = "green"

    elif e.char.lower() == "f":
        cursor_obj["colour"] = "blue"
    

    elif cursor_loc[1] != "wall":
        if e.char.lower() == "z":
            cursor_obj["style"] = "antique"

        elif e.char.lower() == "x":
            cursor_obj["style"] = "retro"

        elif e.char.lower() == "c":
            cursor_obj["style"] = "modern"

        elif e.char.lower() == "v":
            cursor_obj["style"] = "unusual"


    redraw = True
    

    


root.bind("<Right>", cursor_next)
root.bind("<Left>", cursor_prev)
root.bind("<Down>", hide_to_do)
root.bind("<Up>", show_to_do)
root.bind("<KeyPress>", handle_keypress)


WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

if WIDTH/HEIGHT - 16/9 > 0.02:
    #Screen is wider than expected
    WIDTH = int(HEIGHT* 16/9)
elif WIDTH/HEIGHT - 16/9 < 0.2:
    #Screen is taller than expected
    HEIGHT = int(WIDTH * 9/16)


#Initialise Canvas
canvas = Image.new(mode= "RGBA", size=(596,336))


#RULES

#check 2 rules are compatable 
def rule_compatability(rule1, rule2):
    if rule1 == rule2:
        return False
    
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
        target = 12
    
        rule = {"obj": True, "room_top": None, "room_left": None, "type": None, "colour": None, "style": None}
    
        rule["room_top"] = choice([True, False, None, None])
        if rule["room_top"] != None:
            obj_variety /= 2
            pos_variety /=2
            if obj_variety * pos_variety <= target:
                raise(VarietyException)

        rule["room_left"] = choice([True, False, None, None])
        if rule["room_left"] != None:
            obj_variety /= 2
            pos_variety /= 2
            if obj_variety * pos_variety <= target: 
                raise(VarietyException) 

        if choice([True, False]):
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
    
    if choice([True, False]):
        # choose option from list for wall option top and remove it
        wall["top"] = wall_option_top.pop(wall_option_top.index(choice(wall_option_top)))
    else:
        # set to None 1/3 of the time
        wall["top"] = None
    

    if choice([True, False]):
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
        wall_option_top.append(wall["top"])
        wall_option_left.append(wall["left"])
        continue
    else: 
        walls.append(wall)

rules += walls

for rule in rules:
    print(rule)



# Evaluate rule
def evaluate_rule(rooms, rule):
    if rule["obj"]:
        req_count = 3 - [rule[j] for j in ["style", "type", "colour"]].count(None)
        best_score = 0
        for room in rooms:
            if not (rule["room_top"] == rooms[room]["top"] or rule["room_top"] == None):
                continue

            if not (rule["room_left"] == rooms[room]["left"] or rule["room_left"] == None):
                continue

            for obj_type in types:
                score = 1
                if not (rule["type"] == obj_type or rule["type"] == None): 
                    score -= (1/req_count)

                if not (rule["style"] == rooms[room][obj_type]["style"] or rule["style"] == None):
                    score -= (1/req_count)
 
                if not (rule["colour"] == rooms[room][obj_type]["colour"] or rule["colour"] == None):
                    score -= (1/req_count)
                
                if score > best_score:
                    best_score = score
                    
        return round(floor(best_score*10)/10,1)

    else:
        for room in rooms:
            if not (rule["top"] == rooms[room]["top"] or rule["top"] == None):
                continue

            if not (rule["left"] == rooms[room]["left"] or rule["left"] == None):
                continue

            if not (rule["colour"] == rooms[room]["colour"]):
                continue

            return 1

        return 0


def create_object(room, rooms, obj_type):
    #Open object or placeholder
    try:
        rooms[room][obj_type]["img"] = Image.open(f'''assets/{room}/{obj_type}/{rooms[room][obj_type]["style"]}/{room}_{rooms[room][obj_type]["style"]}_{rooms[room][obj_type]["colour"]}_{obj_type}.png''')
    except FileNotFoundError:
        print(f'''Failed opening: assets/{room}/{obj_type}/{rooms[room][obj_type]["style"]}/{room}_{rooms[room][obj_type]["style"]}_{rooms[room][obj_type]["colour"]}_{obj_type}.png falling back to assets/placeholder.png''')
        rooms[room][obj_type]["img"] = Image.open(f'''assets/placeholder.png''')

    #Paste (With Alpha Mask), to the top left of room (TEMP LOCATION)
    try:
        Image.Image.paste(canvas, rooms[room][obj_type]["img"], (rooms[room][obj_type]["xpos"]+rooms[room]["xpos"]-rooms[room][obj_type]["img"].size[0]+1, rooms[room][obj_type]["ypos"]+rooms[room]["ypos"]-rooms[room][obj_type]["img"].size[1]+1), rooms[room][obj_type]["img"].convert("RGBA"))
    except KeyError:
        pass


def create_rooms(rooms):
    for room in rooms.keys():
        #Open room (or use placeholder):
        try:
            rooms[room]["img"]= Image.open(f'''assets/{room}/room/{room}_{rooms[room]["colour"]}.png''')
        except FileNotFoundError:
            try:
                print(f'''Failed opening: assets/{room}/room/{room}_{rooms[room]["colour"]} falling back to assets/{room}/room/{room}_blank.png''')
                rooms[room]["img"] = Image.open(f'''assets/{room}/room/{room}_blank.png''')
            except FileNotFoundError:
                print(f'''Failed opening: assets/{room}/room/{room}_placeholder.png falling back to assets/room_blank.png''') 
                rooms[room]["img"] = Image.open(f'''assets/room_placeholder.png''')

        #Resize Room (Rooms are upsampled 2x to make art easier) with Nearest Neighbour Resampling (best for pixel art)
        rooms[room]["img"] = rooms[room]["img"].resize((192, 128), Image.NEAREST)
        

        #Place in middle
        xpos = 298
        if rooms[room]["left"]:
            xpos -= 192
        
        #Place on floor (or on other room)
        ypos = 80
        if not rooms[room]["top"]:
            ypos += 128
        
        #Paste onto canvas (With transparency)
        Image.Image.paste(canvas, rooms[room]["img"], (xpos, ypos), rooms[room]["img"].convert("RGBA"))

        rooms[room]["xpos"] = xpos
        rooms[room]["ypos"] = ypos

        #Create objects
        for obj in types:
            create_object(room, rooms, obj)
        


canvas_tk = ImageTk.PhotoImage(canvas.resize((WIDTH, HEIGHT), Image.NEAREST))
canvas_label = tk.Label()
canvas_label.place(x=0, y=0)


#Place Quit Button
quit = tk.Button(root, text="QUIT", bg="darkred", fg = "white", command=destroy_window)
quit.place(x = 0, y = 0) #Ugly and Hardcoded, fix later

def draw_canvas():
    global canvas, canvas_label, canvas_tk, cursor_order, cursor_pos, to_do, to_do_pos, update_to_do, sleep_frames
    
    #Load and Place Background
    try:
        back_img = Image.open('assets/back.png') # If house.png does not open -
    except FileNotFoundError:
        print(f'Failed opening: assets/back.png, falling-back to: assets/back_placeholder.png')
        back_img = Image.open('assets/back_placeholder.png') # - Use placeholder

    #Place background on canvas
    back_img = back_img.resize((596, 336), Image.NEAREST)
    Image.Image.paste(canvas, back_img, (0, 0))


    #Draw rooms and objects onto canvas
    create_rooms(rooms)
    
    #Draw cursor
    cursor_loc = cursor_order[cursor_pos]
    cursor_room = rooms[cursor_loc[0]]
    cursor_obj = cursor_room[cursor_loc[1]] if cursor_loc[1] != "wall" else cursor_room

    if cursor_obj["img"].size == (32,32):
        cursor_img = Image.open("assets/cursor_square.png")
        cur_xpos = cursor_obj["xpos"]-31+cursor_room["xpos"]
        cur_ypos = cursor_obj["ypos"]-31+cursor_room["ypos"]

    elif cursor_obj["img"].size == (32,64):
        cursor_img = Image.open("assets/cursor_tall.png")
        cur_xpos = cursor_obj["xpos"]-31+cursor_room["xpos"]
        cur_ypos = cursor_obj["ypos"]-63+cursor_room["ypos"]

    elif cursor_obj["img"].size == (64,32):
        cursor_img = Image.open("assets/cursor_wide.png")
        cur_xpos = cursor_obj["xpos"]-63+cursor_room["xpos"]
        cur_ypos = cursor_obj["ypos"]-31+cursor_room["ypos"]
    
    else:
        cursor_img = Image.open("assets/cursor_room.png")
        cur_xpos = cursor_obj["xpos"]
        cur_ypos = cursor_obj["ypos"]

    
    Image.Image.paste(canvas, cursor_img, (cur_xpos,cur_ypos), cursor_img.convert("RGBA"))
    
    if update_to_do:
        update_to_do = False
        #draw to do list
        to_do = Image.open("assets/to_do.png").convert("RGBA")
    
        stuff = Image.open("assets/to_do_stuff.png")
        Image.Image.paste(to_do, stuff, (11,20), stuff.convert("RGBA"))
    
        n_smileys = len(glob.glob("assets/smileys/*.png"))
        squiggle_y = 38
    
        drawn_wall_label = False

        for rule in rules: 
            if not rule["obj"] and not drawn_wall_label:
                drawn_wall_label = True
                walls = Image.open("assets/to_do_walls.png")
                Image.Image.paste(to_do, walls, (11,squiggle_y), walls.convert("RGBA"))
                squiggle_y += 18

            squiggle = Image.open(choice(glob.glob("assets/squiggles/*.png")))
            Image.Image.paste(to_do, squiggle, (11,squiggle_y), squiggle.convert("RGBA"))

            rule_score = evaluate_rule(rooms, rule)

            smiley = Image.open(f"assets/smileys/smiley_{round(rule_score * (n_smileys-1))}.png")
            Image.Image.paste(to_do, smiley, (11,squiggle_y), smiley.convert("RGBA"))

            squiggle_y += 18


    Image.Image.paste(canvas, to_do, (576-int(92*to_do_pos),0), to_do.convert("RGBA"))


    sleep = Image.open("assets/sleep.png")

    Image.Image.paste(canvas, sleep, (0, 0-int(336*(1-sleep_pos))), sleep.convert("RGBA"))

    # sleeping
    sleep_rec = Image.new("RGBA", canvas.size)
    ImageDraw.Draw(sleep_rec, "RGBA").rectangle([(0,0),(596,336)], fill=(0,0,0,int(-(0.08*(sleep_frames)-4)**4+255)))
    Image.Image.paste(canvas, sleep_rec, (0,0), sleep_rec.convert("RGBA"))

    if sleep_frames > 0:
        sleep_frames -= 1
    
    if sleep_frames == 10:
        show_to_do()

    if sleep_frames == 50:
        hide_sleep()
        update_to_do = True

    #Convert Canvas to Tk Label and draw to screen
    #Resample to screen size using NN
    canvas_tk = ImageTk.PhotoImage(canvas.resize((WIDTH, HEIGHT), Image.NEAREST))

    canvas_label.config(image = canvas_tk)

    
draw_canvas()




#Mainloop
x = 0
while mainloop:
    root.update_idletasks()
    root.update()
    
    if redraw or sleep_frames > 0:
        draw_canvas()
        redraw = False

    x += 1

root.destroy()

