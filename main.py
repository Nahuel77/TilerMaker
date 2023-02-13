import tkinter as tk
from tkinter import *
from tkinter import colorchooser
from PIL import Image, ImageGrab, ImageTk

grid_size = 20
current_color = "black"
fill = False
old_color = ""

class CanvasDraw:
	def __init__ (self, canvas, grid_size, current_color, fill, old_color):
		self.canvas = canvas
		self.grid_size = grid_size
		self.current_color = current_color
		self.fill = fill

	def c_draw(self, event):
		x = (event.x // self.grid_size) * self.grid_size
		y = (event.y // self.grid_size) * self.grid_size
		self.canvas.create_rectangle(x, y, x + self.grid_size, y + self.grid_size, fill=self.current_color, outline=self.current_color)
"""		if fill == False:
			self.canvas.create_rectangle(x, y, x + self.grid_size, y + self.grid_size, fill=self.current_color, outline=self.current_color)
		else:
			id = self.canvas.find_closest(x, y, halo=1)
			old_color = self.canvas.itemcget(id, "fill")
			self.flood_fill(id, old_color, self.current_color)

	def flood_fill(self, id, old_color, current_color):
		if self.canvas.itemcget(id, "fill") != old_color:
			return
		self.canvas.itemconfig(id, fill=current_color)
		id_right = self.canvas.find_closest(self.canvas.coords(id)[0]+self.grid_size, self.canvas.coords(id)[1], halo=1)
		id_left = self.canvas.find_closest(self.canvas.coords(id)[0]-self.grid_size, self.canvas.coords(id)[1], halo=1)
		id_up = self.canvas.find_closest(self.canvas.coords(id)[0], self.canvas.coords(id)[1]-self.grid_size, halo=1)
		id_down = self.canvas.find_closest(self.canvas.coords(id)[0], self.canvas.coords(id)[1]+self.grid_size, halo=1)
		self.flood_fill(id_right, old_color, current_color)
		self.flood_fill(id_left, old_color, current_color)
		self.flood_fill(id_up, old_color, current_color)
		self.flood_fill(id_down, old_color, current_color)"""

root = tk.Tk()
root.configure(bg="#525365")
root.state("zoomed")
root.resizable(False, False)
root.geometry("800x500")

##############################################
###############canvas-1#######################
canvas1 = tk.Canvas(root, width=317, height=317)
canvas_width = canvas1.winfo_width()
canvas_height = canvas1.winfo_height()
canvas1.pack(side="left", anchor='nw', padx=10, pady=10)

canvas1_draw = CanvasDraw(canvas1, grid_size, current_color, fill, old_color)
canvas1.bind("<Button-1>", canvas1_draw.c_draw)
canvas1.bind("<B1-Motion>", canvas1_draw.c_draw)

##############################################
###############canvas-2#######################
canvas2 = tk.Canvas(root, width=317, height=317)
canvas_width = canvas2.winfo_width()
canvas_height = canvas2.winfo_height()
canvas2.pack(side="left", anchor='nw', padx=10, pady=10)

canvas2_draw = CanvasDraw(canvas2, grid_size, current_color, fill, old_color)
canvas2.bind("<Button-1>", canvas2_draw.c_draw)
canvas2.bind("<B1-Motion>", canvas2_draw.c_draw)

##############################################
###############paleta-colores#################
def seleccionar_color():
	global current_color
	color = colorchooser.askcolor()
	current_color = color[1]
	frame.config(bg=color[1])
	canvas1_draw.current_color = current_color
	canvas2_draw.current_color = current_color

frame = tk.Frame(root, bg='white', width=100, height=100)
frame.pack(side="top", anchor="nw", padx=10, pady=10)

btn_color = tk.Button(root, text='Seleccionar color', command=seleccionar_color)
btn_color.pack(side="top", anchor="nw", padx=10, pady=10)

##############################################
###############btn-relleno####################
"""def fill_status():
	global fill
	fill = not fill

btn_relleno = tk.Button(root, text='Fill', command=fill_status)
btn_relleno.configure(width=13)
btn_relleno.pack(side="top", anchor="ne", padx=10, pady=10)"""

##############################################
###############btn-build######################
def build():
	x = root.winfo_rootx() + canvas1.winfo_x()
	y = root.winfo_rooty() + canvas1.winfo_y()
	w = canvas1.winfo_width()
	h = canvas1.winfo_height()
	im1 = ImageGrab.grab((x, y, x + w, y + h))

	x = root.winfo_rootx() + canvas2.winfo_x()
	y = root.winfo_rooty() + canvas2.winfo_y()
	w = canvas2.winfo_width()
	h = canvas2.winfo_height()
	im2 = ImageGrab.grab((x, y, x + w, y + h))

	result = Image.new("RGB", (600, 200))
	result.paste(im1, (0, 0))
	result.paste(im2, (300, 0))

	result.save("dibujos.png")

	label = Label(root, image=img)
	label.pack()

btn_build = tk.Button(root, text = "Build", command=build)
btn_build.configure(width=13)
btn_build.pack(side="top", anchor="nw", padx=10, pady=10)

##############################################
###############btn-build######################
im = Image.open("dibujos.png")
im = im.resize((150, 100), resample=Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(im)

##############################################
root.mainloop()