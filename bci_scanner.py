# bci_scanner.py
# Scanning Board — Demo Mode

import time
import threading

import PySimpleGUI as sg
try:
    import serial
except Exception:
    serial = None

# === SETTINGS  ===
COM_PORT = '/dev/cu.usbserial-A5069RR4'   # e.g. '/dev/cu.usbserial-A5069RR4' or 'COM3'. Set to None to disable Arduino comms.
BAUD = 115200

# SLOWER TIMINGS 
ROW_TIME = 2.5   
COL_TIME = 1  
SELECTION_FLASH = 0.5  


TARGET_SENTENCE = "SHILPA"




# Keyboard layout (rows)
KEY_ROWS = [
    list("ABCDEF"),
    list("GHIJKL"),
    list("MNOPQR"),
    list("STUVWX"),
    list("YZ.,? "),
    ['SPACE','BKSP','DONE']
]

# === Serial port open (optional) ===
ser = None
if COM_PORT and serial:
    try:
        ser = serial.Serial(COM_PORT, BAUD, timeout=0.1)
        print("Opened serial port:", COM_PORT)
    except Exception as e:
        print("Could not open serial port:", e)
        ser = None

def arduino_send_selection():
    if ser and ser.is_open:
        try:
            ser.write(b'S')
        except Exception:
            pass

# === Build GUI ===

sg.theme('DefaultNoMoreNagging') if hasattr(sg, 'theme') else None

keyboard_rows = []
for r in KEY_ROWS:
    row_elems = []
    for c in r:
        key = f"KEY_{c}"
        if c == 'SPACE':
            disp = 'SPACE'
        elif c == 'BKSP':
            disp = 'BKSP'
        elif c == 'DONE':
            disp = 'DONE'
        else:
            disp = c
        row_elems.append(sg.Button(disp, size=(8,2), key=key, pad=(3,3)))
    keyboard_rows.append(row_elems)

layout = [
    [sg.Text("Scanning Board", font=("Helvetica",18), justification='center', expand_x=True)],
    [sg.Text("Typed:", size=(6,1)), sg.Multiline("", size=(60,6), key='-OUTPUT-', disabled=True)],
    *keyboard_rows,
    [sg.Button("Start Demo"), sg.Button("Stop Demo"), sg.Button("Exit")]
]

window = sg.Window("Scanning Board", layout, finalize=True)

# map for easy update
button_map = {}
for r_idx, row in enumerate(KEY_ROWS):
    for c_idx, ch in enumerate(row):
        button_map[(r_idx, c_idx)] = window[f"KEY_{ch}"]

running = False
demo_thread = None

def demo_loop():
    global running
    typed = ""
    target = TARGET_SENTENCE.upper()
    idx = 0
    while running and idx < len(target):
        for r_idx, row in enumerate(KEY_ROWS):
            if not running or idx >= len(target): break
            # highlight row (darker background)
            for c_idx, ch in enumerate(row):
                button_map[(r_idx, c_idx)].update(button_color=('black','lightgrey'))
            window.refresh()
            next_char = target[idx]
            next_char = ' ' if next_char == ' ' else next_char
            # check if target char in this row
            char_in_row = False
            for c_idx, ch in enumerate(row):
                if ch == 'SPACE' and next_char == ' ':
                    char_in_row = True
                    char_pos = c_idx
                    break
                if len(ch) == 1 and ch == next_char:
                    char_in_row = True
                    char_pos = c_idx
                    break
            if char_in_row:
                # column scanning within row
                for c_idx, ch in enumerate(row):
                    if not running or idx >= len(target): break
                    for cc in range(len(row)):
                        if cc == c_idx:
                            button_map[(r_idx, cc)].update(button_color=('white','green'))
                        else:
                            button_map[(r_idx, cc)].update(button_color=('black','lightgrey'))
                    window.refresh()
                    time.sleep(COL_TIME)
                    select_this = False
                    if ch == 'SPACE' and target[idx] == ' ':
                        select_this = True
                    elif len(ch) == 1 and ch == target[idx]:
                        select_this = True
                    if select_this:
                        # flash selection
                        button_map[(r_idx, c_idx)].update(button_color=('white','red'))
                        window.refresh()
                        # send selection to Arduino (LED blink)
                        arduino_send_selection()
                        # append typed char
                        if ch == 'SPACE':
                            typed += ' '
                        elif ch == 'BKSP':
                            typed = typed[:-1]
                        elif ch == 'DONE':
                            pass
                        else:
                            typed += ch
                        window['-OUTPUT-'].update(typed)
                        time.sleep(SELECTION_FLASH)
                        idx += 1
                        break
                # restore row colors
                for c_idx, ch in enumerate(row):
                    button_map[(r_idx, c_idx)].update(button_color=('white','black'))
                window.refresh()
            else:
                # row not containing target — keep highlighted briefly
                time.sleep(ROW_TIME)
            # clear row highlight
            for c_idx, ch in enumerate(row):
                button_map[(r_idx, c_idx)].update(button_color=('white','black'))
            window.refresh()
    # finished
    running = False

# main event loop
while True:
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED or event == "Exit":
        running = False
        break
    if event == "Start Demo":
        if not running:
            running = True
            demo_thread = threading.Thread(target=demo_loop, daemon=True)
            demo_thread.start()
    if event == "Stop Demo":
        running = False

if ser and ser.is_open:
    ser.close()
window.close()
