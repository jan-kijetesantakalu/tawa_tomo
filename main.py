global WIDTH, HEIGHT, canvas, canvas_label, canvas_tk, to_do, devlog, cursor_pos, gameloop, to_do_pos, to_do_after_id, update_to_do, sleep_pos, sleep_after_id, sleep_time, days, num_rules, num_wall_rules, setup_scroll, title_loop, mainloop, info_pos, info_after_id, win, win_after_id, title_extras, noise, ramp_noise, gallery, gallery_idx, gallery_cloud, SERVER, SERVER_UP, server_cache, top_sneaky_pos, top_sneaky_after_id, ramp_noise_devlog #, SCALE

REPO = "jan-kijetesantakalu/tawa_tomo"
SERVER = 'http://many-wholesome.co.uk:5001'

import tkinter as tk
from random import randint, choice
from PIL import Image, ImageTk, ImageDraw, ImageFont
import glob, sys, os, time, requests, datetime, json, socket, copy
import numpy as np

if "-h" in sys.argv or "--help" in sys.argv:
    print("Options:\n--server http[s]://hostname.tld:PORT/root | Specify remote server\n--noserver | disable internet features\n--help | -h | print this message\n\n")
    exit()

if "--server" in sys.argv:
    try:
        SERVER = sys.argv[sys.argv.index("--server") + 1]
    except:
        print("No argument provided for --server")

if "--noserver" in sys.argv:
    SERVER = None

print(f"using remote server: {SERVER}")

mainloop = True




#https://stackoverflow.com/questions/3764291/how-can-i-see-if-theres-an-available-and-active-network-connection-in-python
def internet(host="api.github.com", port=443, timeout=3):
    global SERVER
    if SERVER == None:
        return False

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print("Network not available:",ex)
        return False

if SERVER != None and ":" not in SERVER:
    print("Server format: http[s]://hostname.tld:PORT/root")
    exit()

if SERVER != None:
    SERVER_UP = internet(SERVER.split(":")[1].replace("//", ""), int(SERVER.split(":")[-1]))
else:
    SERVER_UP = False

if SERVER != None:
    print(f"{SERVER.split(":")[1].replace("//", "")} port {int(SERVER.split(":")[-1])} status", "up" if SERVER_UP else "down")

if not os.path.isdir("assets"):
    print("./assets not found. Are you running from the correct location?")
    exit()

if os.path.isfile(".git/HEAD"):
    VERSION = ""
    ONLINE_VERSION = ""
    with open("version") as ver:
        VERSION = ver.readline().rstrip()

    try:
        with open(os.path.join(".git", "HEAD")) as head:
            with open(os.path.join(".git", head.readline().split(":")[1][1:].rstrip())) as h:
                HASH = h.readline().rstrip()
                VERSION += ":" + HASH     
    except OSError:
        print("Error accessing git HEAD")

    try:    
        if internet() and ":" in VERSION:

            ONLINE_VERSION = requests.get(f"https://raw.githubusercontent.com/{REPO}/main/version").text
            ONLINE_HASH = requests.get(f"https://api.github.com/repos/{REPO}/commits").json()[0]["sha"]
            ONLINE_VERSION += ":" + ONLINE_HASH
    
    
            if VERSION != ONLINE_VERSION:
                print(f"Local version {VERSION} does not match remote {ONLINE_VERSION}\nUpgrade with:\ngit pull")
                input("Press enter to continue anyway.")
            else:
                print(f"Local version: {VERSION} matches remote.")
        else:  
            print(f"Can't check update status, Local version: {VERSION}.")
    except Exception as e:
            print(f"{e}\nCan't acess git repo {REPO}, Local version: {VERSION}")

else:
    print(f"Not running in git repository.\nCan't check update status or version.")
    


#Disable printing if not in debug mode
if len(sys.argv) <= 1 or not "--debug" in sys.argv:
    sys.stdout = open(os.devnull, 'w')


def save_house(r, rule):
    save = []
    rooms_t = copy.deepcopy(r)
    for i in rooms_t:
        for j in rooms_t[i].copy():
            if j not in ["colour", "top", "left"] + TYPES:
                del rooms_t[i][j]
                continue
            if hasattr(rooms_t[i][j], '__iter__') and type(rooms_t[i][j]) != str:
                for k in rooms_t[i][j].copy():
                    if k not in ["colour", "style", "xpos", "ypos"]:
                        del rooms_t[i][j][k]
                        continue
            print("saving:", i, j, rooms_t[i][j])

    save.append(rooms_t)
    print("\nsaving: ".join([str(i) for i in rule]))
    save.append(rule)
    if not os.path.isdir("saved_houses"):
        os.mkdir("saved_houses")
    with open(os.path.join("saved_houses", datetime.datetime.now().strftime('%Y-%m-%d@%H-%M') +".tomo"), "w") as f:
        f.write(json.dumps(save))

gameloop = True
title_extras = False
setup_loop = True
setup_scroll = -336
server_cache = {}

img_cache = {}

def exit_loop():
    global gameloop, setup_loop, title_loop, mainloop
    gameloop = False
    setup_loop = False
    title_loop = False
    mainloop = False

#Create Canvas Image
canvas = Image.new(mode= "RGBA", size=(596,336))


def open_asset(asset = "placeholder", bypass_cache = False):
    global img_cache
    try:
        if asset not in img_cache or bypass_cache:
            img = Image.open(os.path.join(f"assets", f"{asset}.png"))
            img_cache[asset] = img
            return img
        else:
            return img_cache[asset]
    except OSError:
        print(f'\nFailed opening: {os.path.join(f"assets", f"{asset}.png")}, falling-back to: {os.path.join("assets","placeholder.png")}')
        if asset not in img_cache:
            try:
                img = Image.open(os.path.join(f"assets","placeholder.png"))
                img_cache[asset] = img
                return img
            except:
                return Image.new(mode = "RGBA", size = (32,32))
        else:
            return img_cache[asset]

def draw_img(img = open_asset("placeholder"), pos = (0, 0), dest = canvas):
    Image.Image.paste(dest, img, pos, img.convert("RGBA"))
    return dest

def draw_asset(asset = "placeholder", pos = (0,0), dest = canvas):
    dest = draw_img(open_asset(asset), pos, dest)
    return dest

#Create Root Window
root = tk.Tk()
root.attributes('-fullscreen', True)
root.protocol("WM_DELETE_WINDOW", exit_loop)
root.title("tawa tomo - jan Kili Lili anu jan Kijetesantakalu")
root.wm_iconphoto(True, ImageTk.PhotoImage(open_asset("icon"))) 


win_after_id = None
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

canvas_tk = ImageTk.PhotoImage(canvas.resize((WIDTH, HEIGHT), Image.NEAREST))
canvas_label = tk.Label()

if WIDTH/HEIGHT - 16/9 > 0.02:
    #Screen is wider than expected
    canvas_label.place(x=int((WIDTH-(HEIGHT * 16/9))/2), y=0)
    WIDTH = int(HEIGHT* 16/9)
elif WIDTH/HEIGHT - 16/9 < 0.2:
    #Screen is taller than expected
    canvas_label.place(x=0, y=int((HEIGHT-(WIDTH*9/16))/2))
    HEIGHT = int(WIDTH * 9/16)
else:
    canvas_label.place(x=0, y=0)

def finalise_canvas():
    global canvas, canvas_label, canvas_tk
    canvas_tk = ImageTk.PhotoImage(canvas.resize((WIDTH, HEIGHT), Image.NEAREST))
    canvas_label.config(image = canvas_tk)



#Initilse Constants

TYPES   = ["lamp", "hanging", "tat"]
COLOURS = ["red", "blue", "green", "yellow"]
STYLES  = ["modern", "antique", "retro", "unusual"]

CURSOR_ORDER = [("bathroom", "wall"), ("bathroom", "hanging"), ("bathroom", "tat"), ("bathroom", "lamp"), 
                ("bedroom", "wall"), ("bedroom", "tat"), ("bedroom", "lamp"), ("bedroom", "hanging"),
                ("lounge", "wall"), ("lounge", "tat"), ("lounge", "hanging"), ("lounge", "lamp"),
                ("kitchen", "wall"), ("kitchen", "lamp"), ("kitchen", "hanging"), ("kitchen", "tat")]


#Initilise Default Values
cursor_pos = 0 # Taken mod 16, the index of the cursor in CURSOR_ORDER

to_do_pos = 1 #float, 0-1 (incl) interpolated the position of the to_do image

update_to_do = False
to_do = open_asset("to_do")

sleep_pos = 0 #float, 0-1 (incl) interpolated the position of the sleep image
sleep_time = 0 #The number of frames to sleep for

info_pos = 0

days = 0 #The number of days passed (in game)

num_rules = 4       #Default values, can be overwritten later
num_wall_rules = 2  #As above

rules = []

win = False
win_pos = 336



#Empty Room Initilisation
rooms = {"bathroom": {}, "bedroom": {}, "kitchen":{}, "lounge": {}} #Contains the rooms
rooms["bathroom"] = {
        "colour": choice(COLOURS), 
                    
        "hanging": {"colour": choice(COLOURS), "style": None, "img": None, "xpos":51, "ypos":95}, 
        "lamp": {"colour": choice(COLOURS), "style": None, "img": None, "xpos":183, "ypos":67},
        "tat": {"colour": choice(COLOURS), "style": None, "img": None, "xpos":103, "ypos":123},
        
        "top": True,
        "left": True,
                    
        "img": None,
        "xpos": None,
        "ypos": None
}

rooms["bedroom"]  = {
       "colour": choice(COLOURS), 
        
        "hanging": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 179, "ypos": 67}, 
        "lamp": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 115, "ypos": 107},
        "tat": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 77, "ypos": 95},
                    
        "top": True,
        "left": False,
                    
        "img": None,
        "xpos": None,
        "ypos": None
}

rooms["kitchen"]  = {
        "colour": choice(COLOURS), 
                     
        "hanging": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 71, "ypos": 59}, 
        "lamp": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 39, "ypos": 86},
        "tat": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 143, "ypos": 86},
                    
        "top": False,
        "left": False,
                    
        "img": None,
        "xpos": None,
        "ypos": None
}

rooms["lounge"]  = {
        "colour": choice(COLOURS), 
        
        "hanging": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 139, "ypos": 63}, 
        "lamp": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 183, "ypos": 123},
        "tat": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 87, "ypos": 123},
                    
        "top": False,
        "left": True,
                    
        "img": None,
        "xpos": None,
        "ypos": None            
}

#check 2 rules are compatable 
def rule_compatability(rule1, rule2):
    if rule1 == rule2:
        return False
    
    if rule1["room_top"] == rule2["room_top"] and rule1["room_top"] != None and rule1["type"] == rule2["type"] and rule1["type"] != None:
        return False

    return True

def create_obj_rules(num_rules):
    global TYPES, COLOURS, STYLES
    #make rules for objects
    rules = []

    type_options = TYPES*2

    class VarietyException(Exception):
        pass

    while len(rules) < num_rules:
        try:
            #magic numbers!
            obj_variety = 192 
            pos_variety = 12
            target = 36
        
            rule = {"obj": True, "room_top": None, "room_left": None, "type": None, "colour": None, "style": None} 
        
            rule["room_top"] = choice([True, False, None, None])
            if rule["room_top"] != None:
                pos_variety /=2
                if obj_variety * pos_variety <= target:
                    raise(VarietyException)

            rule["room_left"] = choice([True, False, None, None])
            if rule["room_left"] != None:
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

            rule["colour"] = choice(COLOURS+([None]))
            if rule["colour"] != None:
                obj_variety /= 4
                if obj_variety * pos_variety <= target:
                    raise(VarietyException) 

            rule["style"] = choice(STYLES+([None]))
            if rule["style"] != None:
                obj_variety /= 4
                if obj_variety * pos_variety <= target:
                    raise(VarietyException)
            
            if rule["type"] != None:
                type_options.append(rule["type"])

            print(f"Continued rule {rule} with total variety {obj_variety * pos_variety} [{obj_variety}, {pos_variety}]")

        except VarietyException:
            comp = True
            for rul in rules:
                if not comp:
                    break
                else:
                    comp = rule_compatability(rule, rul)
                    if not comp:
                        print(f"Passed rule {rule}, incompatible with {rul}")
            if comp:
                rules.append(rule)   
            elif rule["type"] != None:
                type_options.append(rule["type"])

            print(f"Added rule {rule} with total variety {obj_variety * pos_variety} [{obj_variety}, {pos_variety}]")
    
    return rules

def create_wall_rules(num_wall_rules):
    global COLOURS
    # make rules for room colour
    walls = []
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

        wall["colour"] = choice(COLOURS)
        
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


    return walls

# Evaluate rule
def evaluate_rule(rooms, rule):
    global TYPES, COLOURS, STYLES
    if rule["obj"]:
        req_count = 3 - [rule[j] for j in ["style", "type", "colour"]].count(None)
        best_score = 0
        for room in rooms:
            if not (rule["room_top"] == rooms[room]["top"] or rule["room_top"] == None):
                continue

            if not (rule["room_left"] == rooms[room]["left"] or rule["room_left"] == None):
                continue

            for obj_type in TYPES:
                score = 1
                if rooms[room][obj_type]["style"] == None:
                    continue

                if not (rule["type"] == obj_type or rule["type"] == None): 
                    score -= (1/req_count)

                if not ((rule["style"] == rooms[room][obj_type]["style"] or rule["style"] == None) and rooms[room][obj_type]["style"] != None):
                    score -= (1/req_count)
 
                if not (rule["colour"] == rooms[room][obj_type]["colour"] or rule["colour"] == None):
                    score -= (1/req_count)
                
                if score > best_score:
                    best_score = score
                    
        return best_score

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


#SETUP SCREEN


def create_sleep_overlay():
    sleep_rec = Image.new("RGBA", canvas.size)
    ImageDraw.Draw(sleep_rec, "RGBA").rectangle([(0,0),(596,336)], fill=(0,0,0,int(-(0.08*(sleep_time*(100/5))-4)**4+255)))
    font = ImageFont.truetype("assets/pixel_font.ttf", 48)
    imgdraw = ImageDraw.Draw(sleep_rec, "RGBA")
    imgdraw.fontmode = "1" 
    imgdraw.text((298,168),f'''DAY {max(days,1)}''', font=font, anchor="mb", fill=(255,255,255,int(-(0.08*(sleep_time*(100/5))-4)**4+255)))
    return sleep_rec


def draw_setup():
    global canvas, canvas_label, canvas_tk, num_rules, num_wall_rules, sleep_time, setup_scroll
    
    draw_asset("back")
    draw_asset("title")


    draw_asset("setup_menu", (0, -setup_scroll))

    draw_asset(f"numbers/number_{num_rules}", (107, 397-setup_scroll))

    draw_asset(f"numbers/number_{num_wall_rules}", (114, 414-setup_scroll))
    
    if sleep_time > 0:
        draw_img(create_sleep_overlay())

    finalise_canvas()

def increment_num_rules():
    global num_rules
    num_rules %= 6
    num_rules += 1

def dincrement_num_rules():
    global num_rules
    if num_rules >= 2:
        num_rules += 5
        num_rules %= 6
    else:
        num_rules = 6


def increment_num_wall_rules():
    global num_wall_rules
    num_wall_rules %= 4
    num_wall_rules += 1


def dincrement_num_wall_rules():
    global num_wall_rules
    if num_wall_rules >= 2:
        num_wall_rules += 3
        num_wall_rules %= 4
    else:
        num_wall_rules = 4

def increment_setup_scroll():
    global setup_scroll
    setup_scroll = min(672, setup_scroll + 24)

def dincrement_setup_scroll():
    global setup_scroll
    setup_scroll = max(0, setup_scroll - 24)

def hide_setup():
    global setup_loop, setup_scroll, gameloop, title_loop, to_do_pos
    if setup_scroll > -336:
        setup_scroll = max(-336, setup_scroll-24)
        root.after(1, hide_setup)
    else:
        gameloop = False
        setup_loop = False
        title_loop = True
        to_do_pos = 15.8

def handle_keypress_setup(e):
    global setup_loop, sleep_time, setup_scroll, gameloop, title_loop, to_do_pos

    if sleep_time > 0:
        return

    elif e.keysym.lower() == "a":
        hide_setup()
    
    elif e.keysym.lower() == "j":
        dincrement_num_rules()

    elif e.keysym.lower() == "l":
        increment_num_rules()

    elif e.keysym.lower() == "i":
        dincrement_setup_scroll()
    
    elif e.keysym.lower() == "k":
        increment_setup_scroll()

    elif e.keysym.lower() == "left":
        dincrement_num_wall_rules()

    elif e.keysym.lower() == "right":
        increment_num_wall_rules()
    
    elif e.keysym.lower() == "up":
        if setup_scroll >= 336:
            sleep_time = 5


def show_info(e=None):
    global info_pos, info_after_id
    
    if info_pos < 1:
        info_pos += 0.03+((1-info_pos)/16)+((1-info_pos)/4)**2
        try:
            root.after_cancel(info_after_id)
        except NameError:
            # if event not defined
            pass
        info_after_id = root.after(1, show_info)
    info_pos = min(info_pos, 1)

def hide_info(e=None):
    global info_pos, info_after_id
    
    if info_pos > 0:
        info_pos -= 0.03+(info_pos/16)+(info_pos/4)**2
        try:
            root.after_cancel(info_after_id)
        except NameError:
            # if event not defined
            pass
        info_after_id = root.after(1, hide_info)
    info_pos = max(info_pos, 0)

def show_top_sneaky(e=None):
    global top_sneaky_pos, top_sneaky_after_id
    if top_sneaky_pos < 1:
        top_sneaky_pos += 0.03+abs((1-top_sneaky_pos)/16)+abs((1-top_sneaky_pos)/4)**2
        try:
            root.after_cancel(top_sneaky_after_id)
        except NameError:
            # if event not defined
            pass
        top_sneaky_after_id = root.after(1, show_top_sneaky)
    if top_sneaky_pos > 1:
        top_sneaky_pos = 1


def hide_top_sneaky(e=None):
    global top_sneaky_pos, top_sneaky_after_id
    if top_sneaky_pos > 0:
        top_sneaky_pos -= 0.03+(top_sneaky_pos/16)+(top_sneaky_pos/4)**2
        try:
            root.after_cancel(top_sneaky_after_id)
        except NameError:
            # if event not defined
            pass
        top_sneaky_after_id = root.after(1, hide_top_sneaky)
    if top_sneaky_pos < 0:
        top_sneaky_pos = 0


def handle_keypress_title(e=None):
    global title_loop, title_extras, noise, ramp_noise, devlog, gallery, gallery_idx, gallery_pos, gallery_cloud, server_cache, SERVER_UP, top_sneaky_pos, ramp_noise_devlog

    if not title_extras:
        if e.keysym.lower() == "a":
            if info_pos < 0.05:
                title_loop = False
            else:
                hide_info(e)

        elif e.keysym.lower() == "s":
            if info_pos < 0.05:
                show_info(e)
            else:
                hide_info(e)

        elif e.keysym.lower() == "d":
            if info_pos == 0:
                ramp_noise = True
            elif info_pos > 0.05:
                hide_info(e)

        elif e.keysym.lower() == "f":
            hide_info(e)
            if info_pos < 0.05: 
                exit_loop()
    else:
        if ramp_noise or ramp_noise_devlog:
            return

        if e.keysym.lower() == "a" and not devlog and top_sneaky_pos < 0.05:
            gallery = not gallery
            server_cache = {}
            
        
        elif e.keysym.lower() == "s" and not gallery and not devlog:
            if top_sneaky_pos < 0.05:
                show_top_sneaky(e)
            else:
                hide_top_sneaky(e)


        elif e.keysym.lower() == "d" and not gallery and not devlog and top_sneaky_pos < 0.05:
            if gallery_pos < 16:
                ramp_noise = True
        
        elif e.keysym.lower() == "f" and not gallery and top_sneaky_pos < 0.05:
            #devlog = not devlog
            ramp_noise_devlog = True

        elif gallery and e.keysym.lower() == "i":
            submit_house()

        elif gallery and e.keysym.lower() == "j":
            gallery_idx-=1
       
        elif gallery and e.keysym.lower() == "l":
            gallery_idx+=1
          
        elif gallery and e.keysym.lower() == "up":
            
            server_cache = {}
            if gallery_cloud == False:
                if SERVER != None:
                    SERVER_UP = internet(SERVER.split(":")[1].replace("//", ""), int(SERVER.split(":")[-1]))
                    print(f"{SERVER.split(":")[1].replace("//", "")} port {int(SERVER.split(":")[-1])} status {SERVER_UP}")

            gallery_cloud = True
        
        elif gallery and e.keysym.lower() == "down":
            gallery_cloud = False
            server_cache = {}
        
        
        
        

def create_to_do():
    #draw to do list
    td = open_asset("to_do", True)

    draw_asset("to_do_stuff", (11,20), td)

    n_smileys = len(glob.glob(os.path.join("assets", "smileys", "*.png")))
    squiggle_y = 38

    drawn_wall_label = False
    
    squiggles = [x for x in range(1,len(glob.glob(os.path.join("assets", "squiggles", "*.png")))+1)]

    for rule in rules: 
        if not rule["obj"] and not drawn_wall_label:
            drawn_wall_label = True
            draw_asset("to_do_walls", (11, squiggle_y), td)
            squiggle_y += 18
        
        if len(squiggles) == 0:
            squiggles = [x for x in range(1,len(glob.glob(os.path.join("assets", "squiggles", "*.png")))+1)]
        
        squig = f"squiggles/squiggle_{squiggles.pop(randint(0, len(squiggles)-1))}"

        draw_asset(squig, (11, squiggle_y), td)

      #  draw_asset(f"smileys/smiley_{round(evaluate_rule(rooms, rule) * (n_smileys-1))}", (11,squiggle_y), td)

        squiggle_y += 18
    
    return td

#gameloop SCREEN

def draw_object(room, rooms, obj_type, blank= True, dest=canvas):
    #Open object or placeholder
    if rooms[room][obj_type]["style"] != None:
        rooms[room][obj_type]["img"] = open_asset(os.path.join(f'{room}/{obj_type}', f'{rooms[room][obj_type]["style"]}', f'{room}_{rooms[room][obj_type]["style"]}_{rooms[room][obj_type]["colour"]}_{obj_type}'))

    elif blank:
        rooms[room][obj_type]["img"] = open_asset("blank")
    else:
        return
    draw_img(rooms[room][obj_type]["img"], (rooms[room][obj_type]["xpos"]+rooms[room]["xpos"]-rooms[room][obj_type]["img"].size[0]+1, rooms[room][obj_type]["ypos"]+rooms[room]["ypos"]-rooms[room][obj_type]["img"].size[1]+1), dest=dest)

def draw_rooms(rooms, blank = True, dest = canvas):
    for room in rooms.keys():
        #Open room (or use placeholder):
        rooms[room]["img"]= open_asset(os.path.join(f'{room}', 'room', f'{room}_{rooms[room]["colour"]}'))

        #Place in middle of canvas
        xpos = 298
        if rooms[room]["left"]:
            xpos -= 192
        
        #Place on floor (or on other room)
        ypos = 80
        if not rooms[room]["top"]:
            ypos += 128
        
        #Paste onto canvas (With transparency)
        draw_img(rooms[room]["img"], (xpos, ypos), dest)

        rooms[room]["xpos"] = xpos
        rooms[room]["ypos"] = ypos

        #Create objects
        for obj in TYPES:
            draw_object(room, rooms, obj, blank, dest)

def create_tv_noise(trans = 255*2):
    img = np.random.rand(336, 596)
    img = Image.fromarray(np.uint8(img*255), 'L').convert("RGBA")
    img = np.array(img)
    img[:,:,3] = np.uint8(np.clip((np.random.rand(336, 596)*trans*2), 0, 255))
    img = Image.fromarray(img, 'RGBA')
    return img        


def update_to_do_status(td):
    n_smileys = len(glob.glob(os.path.join("assets", "smileys", "*.png")))
    squiggle_y = 38
    win = True
    drawn_wall_label = False
    print("\nupdating to_do status:")
    for rule in rules: 
        if not rule["obj"] and not drawn_wall_label:
            drawn_wall_label = True
            squiggle_y += 18
        
        room_score = evaluate_rule(rooms, rule)
        if room_score < 1:
            win = False
        print(rule, "=>", room_score, f"[{round(room_score * (n_smileys-1))}]")

        draw_asset(os.path.join("smileys", f"smiley_{round(room_score * (n_smileys-1))}"), (11,squiggle_y), td)

        squiggle_y += 18
    return td, win

def create_cursor():
    global cursor_pos
    #create cursor
    cursor_loc = CURSOR_ORDER[cursor_pos]
    cursor_room = rooms[cursor_loc[0]]
    cursor_obj = cursor_room[cursor_loc[1]] if cursor_loc[1] != "wall" else cursor_room

    if cursor_obj["img"].size == (32,32):
        if cursor_obj["style"] == None:
            cursor_img = [open_asset(os.path.join("cursor", "cursor_square"))]
        else:
            cursor_img =[open_asset(os.path.join("cursor", f"cursor_square_{cursor_obj['colour']}")), open_asset(os.path.join("cursor", f"cursor_square_{cursor_obj['style']}"))]
        cur_xpos = cursor_obj["xpos"]-31+cursor_room["xpos"]
        cur_ypos = cursor_obj["ypos"]-31+cursor_room["ypos"]

    elif cursor_obj["img"].size == (32,64):
        if cursor_obj["style"] == None:
            cursor_img = [open_asset(os.path.join("cursor", "cursor_tall"))]
        else:
            cursor_img =[open_asset(os.path.join("cursor", f"cursor_tall_{cursor_obj['colour']}")), open_asset(os.path.join("cursor", f"cursor_tall_{cursor_obj['style']}"))]
        cur_xpos = cursor_obj["xpos"]-31+cursor_room["xpos"]
        cur_ypos = cursor_obj["ypos"]-63+cursor_room["ypos"]

    elif cursor_obj["img"].size == (64,32):
        if cursor_obj["style"] == None:
            cursor_img = [open_asset(os.path.join("cursor","cursor_wide"))]
        else:
            cursor_img =[open_asset(os.path.join("cursor", f"cursor_wide_{cursor_obj['colour']}")), open_asset(os.path.join("cursor", f"cursor_wide_{cursor_obj['style']}"))]
        cur_xpos = cursor_obj["xpos"]-63+cursor_room["xpos"]
        cur_ypos = cursor_obj["ypos"]-31+cursor_room["ypos"]
    
    else:
        cursor_img = [open_asset(os.path.join("cursor",f"cursor_room_{cursor_obj['colour']}"))]
        cur_xpos = cursor_obj["xpos"]
        cur_ypos = cursor_obj["ypos"]
    
    return cursor_img, (cur_xpos, cur_ypos)


def draw_canvas():
    global canvas, canvas_label, canvas_tk, cursor_pos, to_do, to_do_pos, update_to_do, sleep_time, days, win, win_pos
    
    #Load and Place Background
    draw_asset("back")

    #Draw rooms and objects onto canvas
    draw_rooms(rooms)

    cursor_img, cursor_drawpos = create_cursor()

    for img in cursor_img:
        draw_img(img, cursor_drawpos)
        
    if update_to_do:
        update_to_do = False
        to_do, win = update_to_do_status(to_do)
        if win:
            save_house(rooms, rules)
            print("all rules satisfied")
    
    draw_img(to_do, (576-int(92*to_do_pos),0))
    
    draw_asset("win_screen", (0, win_pos))
    if days < 10:
        draw_asset(os.path.join("numbers", f"number_{days}"), (392, win_pos+208))
    else:
        draw_asset(os.path.join("numbers", f"number_{str(days)[0]}"), (386, win_pos+208))
        draw_asset(os.path.join("numbers", f"number_{str(days)[1]}"), (398, win_pos+209))
    
    if win: 
        preview = Image.new(mode = "RGBA", size = canvas.size)
        draw_asset("back", dest=preview)
        draw_rooms(rooms, blank=False, dest=preview)
        preview = preview.resize((298, 168), Image.LANCZOS)
        draw_img(preview, (4, win_pos+375))
        draw_asset("win_paperclip", (0, win_pos+371))

        if win and sleep_time <= 0.5 and win_pos > 0:
            win_pos = max(win_pos-24, 0)

    draw_asset(os.path.join(f"sleep", f"sleep_{rooms['bedroom']['colour']}"), (0, -24+int(360*(1-sleep_pos))))

    if sleep_time > 0:
        # sleeping
        draw_img(create_sleep_overlay())
    
    finalise_canvas()


def cursor_next(e):
    global cursor_pos
    if e != None and sleep_time > 0:
        return
    cursor_pos += 1
    cursor_pos %= 16

def cursor_prev(e):
    global cursor_pos
    if e != None and sleep_time > 0:
        return
    cursor_pos -= 1
    cursor_pos %= 16

def cursor_room_next(e):
    global cursor_pos
    if e != None and sleep_time > 0:
        return
    cursor_pos += 8
    cursor_pos %= 16

def hide_to_do(e=None):
    global to_do_pos, to_do_after_id    
    if e != None and sleep_time > 0:
        return
    
    if to_do_pos > 0.01:    
        to_do_pos -= 0.01+(to_do_pos/12)+(to_do_pos/4)**1.5
        try:
            root.after_cancel(to_do_after_id)
        except NameError:
            # if event not defined
            pass
        to_do_after_id = root.after(1, hide_to_do)

def show_to_do(e=None):
    global to_do_pos, to_do_after_id    
    if e != None and sleep_time > 0:
        return
    
    if to_do_pos < 0.99:
        to_do_pos += 0.01+((1-to_do_pos)/12)+((1-to_do_pos)/4)**1.5
        try:
            root.after_cancel(to_do_after_id)
        except NameError:
            # if event not defined
            pass
        to_do_after_id = root.after(1, show_to_do)
   

def hide_sleep(e=None):
    global sleep_pos, sleep_after_id
    if e != None and sleep_time > 0:
        return
    
    show_to_do()

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
    global sleep_pos, sleep_after_id, sleep_time

    if e != None and sleep_time > 0:
        return 
    
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


def hide_quit(e=None):
    global to_do_pos, to_do_after_id    
    if e != None and sleep_time > 0:
        return
    
    if to_do_pos > 1:    
        to_do_pos -= 0.01+((to_do_pos-1)/12)+((to_do_pos-1)/4)**1.5
        try:
            root.after_cancel(to_do_after_id)
        except NameError:
            # if event not defined
            pass
        to_do_after_id = root.after(1, hide_quit)


def show_quit(e=None):
    global to_do_pos, to_do_after_id    
    if e != None and sleep_time > 0:
        return
    
    if to_do_pos < 2.75:
        to_do_pos += 0.01+((2.75-to_do_pos)/12)+((2.75-to_do_pos)/4)**1.5
        try:
            root.after_cancel(to_do_after_id)
        except NameError:
            # if event not defined
            pass
        to_do_after_id = root.after(1, show_quit)


def quit_to_title(e=None):
    global to_do_pos, to_do_after_id, gameloop, setup_loop, title_loop, win_pos, win
    if e != None and sleep_time > 0:
        return
    
    if win:
        win_pos = min(win_pos+72, 336)

    if to_do_pos < 15.4:
        to_do_pos += 0.001+((to_do_pos)/8)+((to_do_pos)/12)**1.5
        try:
            root.after_cancel(to_do_after_id)
        except NameError:
            # if event not defined
            pass 
        to_do_after_id = root.after(1, quit_to_title)
    
    if to_do_pos > 5:
        gameloop = False
        setup_loop = True
        title_loop = True


def commit_sleep():
    global sleep_time
    sleep_time = 5
    
def show_win():
    global win_pos, win_after_id
    if win:
        win_pos = min(win_pos+48, 336)
        try:
            root.after_cancel(win_after_id)
            win_after_id = None
        except:
            pass
        win_after_id = root.after(1, show_win)

def hide_win():
    global win_after_id
    try:
        root.after_cancel(win_after_id)
        win_after_id = None
    except:
        pass
def handle_keypress(e):
    global cursor_pos, sleep_pos, sleep_time, to_do_pos, win, win_pos

    if win:
        if e.keysym.lower() == "i":
            if win_pos + 24 <= 0:
                win_pos+=24
        elif e.keysym.lower() == "k":
            if win_pos - 24 >= -297:
                win_pos-=24
        elif e.keysym.lower() == 'down':
            show_win()
        elif e.keysym.lower() == 'up':
            hide_win()
        elif e.keysym.lower() in ["a", "s", "d", "f", "z", "x", "c", "v"]:
            quit_to_title()
        return
     
    if sleep_time > 0:
        return

    cursor_loc = CURSOR_ORDER[cursor_pos]
    cursor_room = rooms[cursor_loc[0]]
    cursor_obj = cursor_room[cursor_loc[1]] if cursor_loc[1] != "wall" else cursor_room
    

    if e.keysym.lower() == "right":
        if to_do_pos > 0.75 and to_do_pos < 1.25:
            hide_to_do(e)
        elif to_do_pos > 1.25:
            hide_quit(e)

    elif e.keysym.lower() == "left":
        if to_do_pos < 0.75:
            show_to_do(e)
        elif to_do_pos > 0.75 and to_do_pos < 1.25:
            show_quit(e)
        elif to_do_pos > 2:
            quit_to_title(e)

    elif e.keysym.lower() == "up":
        if sleep_pos > 0.75:
            commit_sleep()
        else:
            show_sleep(e)

    elif e.keysym.lower() == "down":
        hide_sleep(e)

    if sleep_pos > 0.75:
        return

    if e.keysym.lower() == "j":
        cursor_prev(e)

    elif e.keysym.lower() == "l":
        cursor_next(e)

    elif e.keysym.lower() in ["i", "k"]:
        cursor_room_next(e)

    elif e.keysym.lower() == "a":
        cursor_obj["colour"] = "red"
    
    elif e.keysym.lower() == "s":
        cursor_obj["colour"] = "yellow"
    
    elif e.keysym.lower() == "d":
        cursor_obj["colour"] = "green"

    elif e.keysym.lower() == "f":
        cursor_obj["colour"] = "blue"
    

    elif cursor_loc[1] != "wall":
        
        if e.keysym.lower() == "z":
            if cursor_obj["style"] == "antique":
                cursor_obj["style"] = None
            else:
                cursor_obj["style"] = "antique"

        elif e.keysym.lower() == "x":
            if cursor_obj["style"] == "retro":
                cursor_obj["style"] = None
            else:
                cursor_obj["style"] = "retro"

        elif e.keysym.lower() == "c":
            if cursor_obj["style"] == "modern":
                cursor_obj["style"] = None
            else:
                cursor_obj["style"] = "modern"

        elif e.keysym.lower() == "v":
            if cursor_obj["style"] == "unusual":
                cursor_obj["style"] = None
            else:
                cursor_obj["style"] = "unusual"

def load_saved_house(index = 0):
    houses = glob.glob(os.path.join("saved_houses", "*.tomo"))
    if len(houses) == 0:
        return None, None
    #print("found saves", houses)
    index %= len(houses)
    #print(houses[index])
    return json.load(open(houses[index])), os.path.split(houses[index])[-1].split(".")[0]


def submit_house():
    global SERVER, gallery_idx, server_cache, SERVER_UP
    server_cache = {}
    if SERVER == None:
        return
    
    SERVER_UP = internet(SERVER.split(":")[1].replace("//", ""), int(SERVER.split(":")[-1]))

    print(f"{SERVER.split(":")[1].replace("//", "")} port {int(SERVER.split(":")[-1])} status {SERVER_UP}")

    if not SERVER_UP:
        return

    dat, fn = load_saved_house(gallery_idx)

    r, rule = dat[0], dat[1]

    save = []
    rooms_t = copy.deepcopy(r)
    for i in rooms_t:
        for j in rooms_t[i].copy():
            if j not in ["colour", "top", "left"] + TYPES:
                del rooms_t[i][j]
                continue
            if hasattr(rooms_t[i][j], '__iter__') and type(rooms_t[i][j]) != str:
                for k in rooms_t[i][j].copy():
                    if k not in ["colour", "style", "xpos", "ypos"]:
                        del rooms_t[i][j][k]
                        continue
            print("saving:", i, j, rooms_t[i][j])

    save.append(rooms_t)
    print("\nsaving: ".join([str(i) for i in rule]))
    save.append(rule)
    x = requests.post(SERVER+"/submit_house", json=save)
    print("sent request:", x.text)


def load_online_house(index=0):
    global server_cache, SERVER_UP
    if SERVER == None:
        return None, None
    if not SERVER_UP:
        return None, None
    if not (index  in server_cache):
        server_cache[index] = requests.get(SERVER+f"/get_house?index={index}").json()
    return server_cache[index], str(hash(str(server_cache[index])))

def create_gallery(index = 0):
    global img_cache, gallery_cloud, SERVER_UP, SERVER

    if not gallery_cloud:
        house, fn = load_saved_house(index)
        if house == None:
            return open_asset("gallery_empty")
    else:
        if SERVER == None:
            return open_asset("gallery_server_error")
        
        try:
            house, fn = load_online_house(index)
            if 'err' in house:
                return open_asset("gallery_server_empty")

            if house == None:
                return open_asset("gallery_server_error")
        
        except Exception as e:
            print("Invalid response:", e)
            SERVER_UP = False
            return open_asset("gallery_server_error")


    if not (fn in img_cache):
        print(f"Creating Gallery {index}","\n", house, "\n", fn)
        gallery = Image.new(mode="RGBA", size=canvas.size)
        rooms, rules = house[0], house[1]
        draw_asset("back", dest=gallery)
        draw_rooms(rooms, blank = False, dest = gallery)
        draw_asset("gallery_local" if not gallery_cloud else "gallery_server", dest = gallery)
        if not gallery_cloud:
            font = ImageFont.truetype("assets/pixel_font.ttf", 16)
            imgdraw = ImageDraw.Draw(gallery, "RGBA")
            imgdraw.fontmode = "1" 
            imgdraw.text((588,20),f'''{fn}''', font=font, anchor="rb", fill=(140,20,20,255))
        img_cache[fn] = gallery

    return img_cache[fn]

to_do_pos = 15.8
top_sneaky_pos = 0 

try:
    #SPLASH SCREEN

    update_count = 0

    start_time = time.time()

    while time.time() - start_time < 3:
        frame_start = time.time()
    
        root.update_idletasks()
        root.update()
    
        draw_asset("splash")
        finalise_canvas()
    
        update_count += 1
        print("FPS", round(1/(time.time() - frame_start), 2), end = "\r")
    

    while mainloop:
        root.unbind("<KeyPress>")
        root.bind("<KeyPress>", handle_keypress_title)

        # title
        title_loop = True
        title_extras = False
        noise = 0
        gallery_idx = 0
        ramp_noise = False
        ramp_noise_devlog = False
        gallery = False
        devlog = False
        server_cache = {}

        gallery_pos = 0
        gallery_cloud = False
        while title_loop and mainloop:
            frame_start = time.time()
            root.update_idletasks()         
            root.update()
            draw_asset("back")
            if not title_extras:
                draw_asset("title")
            else:
                draw_asset("title_extras")
            
            draw_img(to_do, (576-int(92*to_do_pos),0))
            
            draw_asset("info_menu", (0, int(360*(1-info_pos))))
           
            draw_asset("top_sneaky", (0, abs(int(336*(1-top_sneaky_pos)))))

            noise = np.clip(noise, 0, 255)
            if ramp_noise or ramp_noise_devlog:
                    noise += (abs(255-noise)**0.5)*3
                    if abs(noise - 255) < 1:
                        if ramp_noise:
                            ramp_noise = False
                            title_extras = not title_extras
                        if ramp_noise_devlog:
                            ramp_noise_devlog = False
                            devlog = not devlog
            else:
                noise -= ((abs(noise))**0.5)*3
            
            if devlog:
                draw_asset("dev_log")
            
            if noise > 0:
                draw_img(create_tv_noise(noise))

            if gallery and gallery_pos < 336:
                gallery_pos += ((336-gallery_pos)**0.5)*2
            elif not gallery and gallery_pos > 0:
                gallery_pos -= ((gallery_pos)**0.5)*2

            draw_img(create_gallery(gallery_idx), (0, int(gallery_pos-336)))
                     
            finalise_canvas()
            update_count += 1
            print("FPS", round(1/(time.time() - frame_start), 2), end = "\r")


        #Initilise Default Values
        cursor_pos = 0 # Taken mod 16, the index of the cursor in CURSOR_ORDER

        to_do_pos = 1 #float, 0-1 (incl) interpolated the position of the to_do image

        update_to_do = False
        to_do = open_asset("to_do")

        sleep_pos = 0 #float, 0-1 (incl) interpolated the position of the sleep image
        sleep_time = 0 #The number of frames to sleep for

        info_pos = 0

        days = 0 #The number of days passed (in game)

        num_rules = 4       #Default values, can be overwritten later
        num_wall_rules = 2  #As above

        rules = []

        win = False
        win_pos = 336

        win_after_id = None


        #Empty Room Initilisation
        rooms = {"bathroom": {}, "bedroom": {}, "kitchen":{}, "lounge": {}} #Contains the rooms
        rooms["bathroom"] = {
                "colour": choice(COLOURS), 
                            
                "hanging": {"colour": choice(COLOURS), "style": None, "img": None, "xpos":51, "ypos":95}, 
                "lamp": {"colour": choice(COLOURS), "style": None, "img": None, "xpos":183, "ypos":67},
                "tat": {"colour": choice(COLOURS), "style": None, "img": None, "xpos":103, "ypos":123},
                
                "top": True,
                "left": True,
                            
                "img": None,
                "xpos": None,
                "ypos": None
        }

        rooms["bedroom"]  = {
            "colour": choice(COLOURS), 
                
                "hanging": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 179, "ypos": 67}, 
                "lamp": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 115, "ypos": 107},
                "tat": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 77, "ypos": 95},
                            
                "top": True,
                "left": False,
                            
                "img": None,
                "xpos": None,
                "ypos": None
        }

        rooms["kitchen"]  = {
                "colour": choice(COLOURS), 
                            
                "hanging": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 71, "ypos": 59}, 
                "lamp": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 39, "ypos": 86},
                "tat": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 143, "ypos": 86},
                            
                "top": False,
                "left": False,
                            
                "img": None,
                "xpos": None,
                "ypos": None
        }

        rooms["lounge"]  = {
                "colour": choice(COLOURS), 
                
                "hanging": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 139, "ypos": 63}, 
                "lamp": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 183, "ypos": 123},
                "tat": {"colour": choice(COLOURS), "style": None, "img": None, "xpos": 87, "ypos": 123},
                            
                "top": False,
                "left": True,
                            
                "img": None,
                "xpos": None,
                "ypos": None            
        }

        top_sneaky_pos = 0 
        setup_scroll = -336


        gameloop = True

        setup_loop = True

        #SETUP

        while setup_loop and mainloop and setup_scroll < 0:
            frame_start = time.time()
            root.update_idletasks()
            root.update()
            draw_setup()
            update_count += 1
            if setup_scroll < 0:
                setup_scroll += 40
            print("FPS", round(1/(time.time() - frame_start), 2), end = "\r")

        root.unbind("<KeyPress>")
        root.bind("<KeyPress>", handle_keypress_setup)
        setup_sleep = True
        while setup_loop and mainloop:
            frame_start = time.time()
            root.update_idletasks()
            root.update()
            draw_setup()
            if sleep_time <= 2.5 and sleep_time > 0:
                setup_loop = False

            if sleep_time > 0:
                sleep_time -= (time.time() - frame_start)
                
            update_count += 1
            print("FPS", round(1/(time.time() - frame_start), 2), end = "\r")

        root.unbind("<KeyPress>")

        rules = create_obj_rules(num_rules) + create_wall_rules(num_wall_rules)

        for rule in rules:
            print(rule)


        to_do = create_to_do()


        #gameloop
        root.bind("<KeyPress>", handle_keypress)


        daycount = False


        while gameloop and mainloop:
            frame_start = time.time()
            root.update_idletasks()
            root.update()
            

            draw_canvas()

            if sleep_time > 0:
                sleep_time -= (time.time() - frame_start)
            else:
                sleep_time = 0
                daycount = False

            if sleep_time <= 0.3 and sleep_time > 0:
                show_to_do()

            if sleep_time <= 2.5 and sleep_time > 0 and not daycount:
                hide_sleep()
                days += 1
                daycount = True
                update_to_do = True

            update_count += 1
            print("FPS", round(1/(time.time() - frame_start), 2), end = "\r") 
except KeyboardInterrupt as KB:
    print(KB)

root.destroy()
