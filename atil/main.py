import tkinter as tk
from tkinter import colorchooser
from PIL import ImageTk, Image, ImageDraw
import queue as Q

root = tk.Tk()
root.geometry("800x600+50+50")
root.config(bg="#C6C6FA")
root.wm_state('zoomed')
root.resizable(False, False)
color = "#000000"

can_width = 16
can_height = 16
pixel_size = 20
pressed = False
fill_status = False
draw_status = True

def start_draw(event):
	global pressed
	pressed = True
	draw(event)

def end_draw(event):
	global pressed
	pressed = False

def draw(event):
	global draw_status, color
	canvas = event.widget
	q, r = event.widget.winfo_pointerxy()
	widget = event.widget.winfo_containing(q, r)
	color_anterior = canvas["background"]
	if draw_status:
		if not(fill_status):
			canvas.configure(bg=color)
			while pressed and isinstance(widget, tk.Canvas):
				widget.configure(bg=color)
				end_draw(event)
				#actualizar el moisaico de muetra
		elif fill_status:
			if color_anterior == color:
				return
			queue = Q.Queue()
			queue.put(widget)
			while not queue.empty():#recordar validar caso en que se comparan Nones (sin color)
				actual_cell = queue.get()
				if actual_cell["background"] != color_anterior:
					continue
				else:
					actual_cell.configure(bg=color)
					q, r = actual_cell.winfo_rootx(), actual_cell.winfo_rooty()
					queue.put(event.widget.winfo_containing(q+pixel_size, r))
					queue.put(event.widget.winfo_containing(q-pixel_size, r))
					queue.put(event.widget.winfo_containing(q, r+pixel_size))
					queue.put(event.widget.winfo_containing(q, r-pixel_size))
	elif not(draw_status):
		canvas = event.widget
		color = color_anterior
		frame.config(bg=color)
		root.config(cursor="arrow")
		draw_status = True

def seleccion_color():
	global color
	picked_color = colorchooser.askcolor()
	color = picked_color[1]
	frame.config(bg=color)

def pen():
	global fill_status
	fill_status = False

def fill():
	global fill_status
	fill_status = True

def eyerdropper():
	global draw_status, color
	draw_status = False
	root.config(cursor="target")

def update_mosaico_muestra():
	global mosaico_muestra
	mosaico_muestra.delete("all")
	# Limpiar el lienzo de muestra
	for i in range(can_width):
		for j in range(can_height):
			celda = celdas[i][j]
			color = celda["background"]
			# Crear un canvas en el lienzo de muestra
			canvas_muestra = tk.Canvas(mosaico_muestra, width=20, height=20, bg=color, highlightthickness=0)
			canvas_muestra.place(x=i*20, y=j*20)

pen_image = Image.open("pen.png")
pen_icon = pen_image.resize((20, 20))
pen_icon_tk = ImageTk.PhotoImage(pen_icon)
btn_pen = tk.Button(root, image=pen_icon_tk, command=pen, bg="#9393EA")
btn_pen.place(x=20, y=21)

color_imagen = Image.open("paleta.png")
color_icon = color_imagen.resize((20, 20))
color_icon_tk = ImageTk.PhotoImage(color_icon)
btn_color = tk.Button(root, image=color_icon_tk, command=seleccion_color, bg="#9393EA")
btn_color.place(x=20, y=51)

fill_image = Image.open("fill.png")
fill_icon = fill_image.resize((20, 20))
fill_icon_tk = ImageTk.PhotoImage(fill_icon)
btn_fill = tk.Button(root, image=fill_icon_tk, command=fill, bg="#9393EA")
btn_fill.place(x=50, y=21)

eyerdropper_image = Image.open("gotero.png")
eyerdropper_icon = eyerdropper_image.resize((20, 20))
eyerdropper_icon_tk = ImageTk.PhotoImage(eyerdropper_icon)
btn_eyerdropper = tk.Button(root, image=eyerdropper_icon_tk, command=eyerdropper, bg="#9393EA")
btn_eyerdropper.place(x=80, y=21)

frame = tk.Frame(root, bg=color, width=26, height=26)
frame.place(x=50, y=51)

mosaico_muestra = tk.Canvas(root, width=can_width*pixel_size, height=can_height*pixel_size, highlightthickness=0)
mosaico_muestra.place(x=900, y=20)

llevar_muestra_image = Image.open("save.png")
llevar_muestra_icon = llevar_muestra_image.resize((20, 20))
llevar_muestra_icon_tk = ImageTk.PhotoImage(llevar_muestra_icon)
btn_guardar = tk.Button(root, image=llevar_muestra_icon_tk, command=update_mosaico_muestra, bg="#9393EA")
btn_guardar.place(x=80, y=51)

celdas = [[None for _ in range(can_height)] for _ in range(can_width)]

for i in range(can_width):
	for j in range(can_height):
		canvas = tk.Canvas(root, width=pixel_size, height=pixel_size, highlightthickness=0)
		canvas.place(x=(i+7)*pixel_size, y=(j+1)*pixel_size)
		canvas.bind("<Button-1>", draw)
		canvas.bind("<B1-Motion>", start_draw)
		canvas.bind("<ButtonRelease-1>", end_draw)
		celdas[i][j] = canvas

for i in range(can_width):
	for j in range(can_height):
		canvas = tk.Canvas(root, width=pixel_size, height=pixel_size, highlightthickness=0)
		canvas.place(x=(i+24)*pixel_size, y=(j+1)*pixel_size)
		canvas.bind("<Button-1>", draw)
		canvas.bind("<B1-Motion>", start_draw)
		canvas.bind("<ButtonRelease-1>", end_draw)

root.mainloop()