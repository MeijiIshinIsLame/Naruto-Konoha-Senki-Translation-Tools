import tkinter as tk
import os
from pathlib import Path
from tkinter import filedialog
from PIL import Image, ImageTk

TILE_SIZE = 32
ROWS = 16
COLS = 24
CLICK_LIMIT = 2

clicks = 0
clicked_labels = []
path = None

root = tk.Tk()
root.title("Graphic Stitcher")


def browse_folder():
    global list_box
    global path
    path = Path(filedialog.askdirectory())
    files = os.listdir(path)
    for file in files:
        list_box.insert("end", file)

def click_limit_reached():
    global clicks
    if clicks >= CLICK_LIMIT:
        return True
    return False

def on_enter(e):
    if not e.widget.clicked:
        e.widget.config(highlightthickness=1, highlightbackground="red")

def on_leave(e):
    if not e.widget.clicked:
        e.widget.config(highlightthickness=0)

def on_click(e):
    global clicks
    global clicked_labels
    if not e.widget.clicked:
        if click_limit_reached():
            pass
        else:
            if len(clicked_labels) < CLICK_LIMIT:
                clicked_labels.append(e.widget)
                e.widget.config(highlightthickness=2, highlightbackground="red")
                clicks += 1
                e.widget.clicked = True
    else:
        e.widget.config(highlightthickness=0)
        clicks = max(0, clicks - 1)
        e.widget.clicked = False
        clicked_labels.remove(e.widget)

def render_image(file, label):
    pil_img = Image.open(file).resize((32, 32))
    tk_img = ImageTk.PhotoImage(pil_img)

    label.config(image=tk_img)
    label.image = tk_img   # 🔑 KEEP A REFERENCE
    
def render_from_selection():
    global clicked_labels
    global list_box
    global path
    if len(clicked_labels) != 1:
        pass
    else:
        file = Path(path / list_box.get(list_box.curselection()))
        tile = clicked_labels[0]
        tile.image_path = file
        render_image(file, tile)
        tile.rotated = 0
        
def rotate_tile():
    global clicked_labels
    if len(clicked_labels) != 1:
        pass
    else:
        label = clicked_labels[0]
        label.rotated += 1
        if label.rotated > 3:
            label.rotated = 0
        img = Image.open(label.image_path).resize((32, 32))
        img = img.rotate(90 * label.rotated)
        tkimg = ImageTk.PhotoImage(img)
        label.config(image=tkimg)
        label.image = tkimg
        

#this doesnt work lol but honestly who cares tbh     
def swap_tile():
    global clicked_labels
    global cells
    if len(clicked_labels) == 2:
        label1 = clicked_labels[0]
        label2 = clicked_labels[1]
        
        for i, item in enumerate(cells):
            if item == clicked_labels[0]:
                cells[i] = clicked_labels[1]
                
        for i, item in enumerate(cells):
            if item == clicked_labels[1]:
                cells[i] = clicked_labels[0]
        
        clicked_labels[0] = label2
        clicked_labels[1] = label1
        print(clicked_labels)

################# FRAMES #################
button_frame = tk.Frame(root)
list_frame = tk.Frame(root, bg="#fff", width=300, height=800)
grid_frame = tk.Frame(root, bg="white")

################# BUTTONS #################
rotate_button = tk.Button(master=button_frame, text="Rotate", command=rotate_tile)
swap_button = tk.Button(master=button_frame, text="Swap Square", command=swap_tile)
browse_button = tk.Button(master=button_frame, text="Browse", command=browse_folder)
render_button = tk.Button(master=button_frame, text="Render Square", command=render_from_selection)

list_box = tk.Listbox(list_frame, selectmode=tk.SINGLE)

img = Image.new('RGB', (TILE_SIZE, TILE_SIZE), color='white')
PLACEHOLDER_IMAGE = ImageTk.PhotoImage(img)

cells = []

for r in range(ROWS):
    row = []
    for c in range(COLS):
        cell = tk.Label(grid_frame, image=PLACEHOLDER_IMAGE, bd=0)
        cell.grid(row=r, column=c)
        cell.grid_propagate(False)
        cell.clicked = False
        cell.bind("<Enter>", on_enter)
        cell.bind("<Leave>", on_leave)
        cell.bind("<Button-1>", on_click)
        row.append(cell)
        print(row)
    cells.append(row)
    
rotate_button.pack(side="left", padx=30)
swap_button.pack(side="left", padx=30)
browse_button.pack(side="left", padx=30)
render_button.pack(side="left", padx=30)
list_box.pack()
button_frame.pack(side="top", padx=10, pady=10)
grid_frame.pack(side="left", padx=0, pady=0)
list_frame.pack(side="right", padx=10, pady=10)

root.mainloop()
