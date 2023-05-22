import tkinter as tk
from tkinter import colorchooser
from PIL import ImageTk, Image, ImageDraw, ImageGrab
import queue as Q

root = tk.Tk()
root.geometry("800x600+50+50")
root.config(bg="#5C5C8C")
root.wm_state('zoomed')
root.resizable(False, False)
color = "#000000"

can_width = 16
can_height = 16
pixel_size = 20
pressed = False
fill_status = False
draw_status = True
clear_status = False

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
	q, r = canvas.winfo_pointerxy()
	widget = canvas.winfo_containing(q, r)
	color_anterior = canvas["background"]
	if draw_status:
		if not(fill_status):
			canvas.configure(bg=color)
			while pressed and isinstance(widget, tk.Canvas):
				widget.configure(bg=color)
				end_draw(event)
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
					queue.put(canvas.winfo_containing(q+pixel_size, r))
					queue.put(canvas.winfo_containing(q-pixel_size, r))
					queue.put(canvas.winfo_containing(q, r+pixel_size))
					queue.put(canvas.winfo_containing(q, r-pixel_size))

	elif not(draw_status):
		if clear_status:
			canvas.configure(bg="SystemButtonFace")
			while pressed and isinstance(widget, tk.Canvas):
				widget.configure(bg="SystemButtonFace")
				end_draw(event)
		else:
			color = color_anterior
			frame.config(bg=color)
			root.config(cursor="arrow")
			draw_status = True

def cancel_tool(event):
	pass

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
	global draw_status, color, clear_status
	draw_status = False
	clear_status = False
	root.config(cursor="target")

def clear():
	global clear_status, draw_status
	draw_status = False
	clear_status = not clear_status
	if clear_status:
		root.config(cursor="X_cursor")
	else:
		root.config(cursor="arrow")
		draw_status = True

def update_mosaico_muestra():
	mosaico_muestra.delete("all")
	for i in range(can_width):
		for j in range(can_height):
			celda1 = celdas[i][j]
			celda2 = celdas2[i][j]
			color1 = celda1["background"]
			color2 = celda2["background"]
			canvas_muestra = tk.Canvas(mosaico_muestra, width=pixel_size, height=pixel_size, bg=color1, highlightthickness=0)
			canvas_muestra.place(x=i*pixel_size, y=j*pixel_size)
			if color2 != "SystemButtonFace":
				canvas2_muestra = tk.Canvas(mosaico_muestra, width=pixel_size, height=pixel_size, bg=color2, highlightthickness=0)
				canvas2_muestra.place(x=i*pixel_size, y=j*pixel_size)

def construir():
	#constructor.delete("all")
	pix = 2
	for i in range(can_width):
		for j in range(can_height):
			celda1 = celdas[i][j]
			color1 = celda1["background"]
			if color1 != "SystemButtonFace":
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i)*pix, y=(j)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width)*pix, y=(j)*pix)
				"""tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width*2)*pix, y=(j)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width*3)*pix, y=(j)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width*4)*pix, y=(j)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width*5)*pix, y=(j)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width*6)*pix, y=(j)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width*7)*pix, y=(j)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width*8)*pix, y=(j)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width*9)*pix, y=(j)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i)*pix, y=(j+can_height)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i)*pix, y=(j+can_height*2)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i)*pix, y=(j+can_height*3)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width)*pix, y=(j+can_height)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width)*pix, y=(j+can_height*2)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width)*pix, y=(j+can_height*3)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width*2)*pix, y=(j+can_height)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width*2)*pix, y=(j+can_height*2)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width*2)*pix, y=(j+can_height*3)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width*3)*pix, y=(j+can_height)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width*3)*pix, y=(j+can_height*2)*pix)
				tk.Canvas(constructor, width=pix, height=pix, bg=color1, highlightthickness=0).place(x=(i+can_width*3)*pix, y=(j+can_height*3)*pix)"""

	#creo una imagen RGBA png
	image = Image.new("RGBA", (67, 67), (255, 0, 0, 0))
	image.save("./mosaico.png", "PNG")
	
	#crear mapa postscript del canvas 1 y 2

	#cargo su data a la imagen y la guardo
	#image.putdata(newData)
	image.save("./mosaico.png", "PNG")

pen_image = Image.open("pen.png")
pen_icon = pen_image.resize((20, 20))
pen_icon_tk = ImageTk.PhotoImage(pen_icon)
btn_pen = tk.Button(root, image=pen_icon_tk, command=pen, bg="#7BC67B")
btn_pen.place(x=20, y=40)

color_imagen = Image.open("paleta.png")
color_icon = color_imagen.resize((20, 20))
color_icon_tk = ImageTk.PhotoImage(color_icon)
btn_color = tk.Button(root, image=color_icon_tk, command=seleccion_color, bg="#7BC67B")
btn_color.place(x=20, y=70)

fill_image = Image.open("fill.png")
fill_icon = fill_image.resize((20, 20))
fill_icon_tk = ImageTk.PhotoImage(fill_icon)
btn_fill = tk.Button(root, image=fill_icon_tk, command=fill, bg="#7BC67B")
btn_fill.place(x=50, y=40)

eyerdropper_image = Image.open("gotero.png")
eyerdropper_icon = eyerdropper_image.resize((20, 20))
eyerdropper_icon_tk = ImageTk.PhotoImage(eyerdropper_icon)
btn_eyerdropper = tk.Button(root, image=eyerdropper_icon_tk, command=eyerdropper, bg="#7BC67B")
btn_eyerdropper.place(x=80, y=70)

frame = tk.Frame(root, bg=color, width=26, height=26)
frame.place(x=50, y=70)

llevar_muestra_image = Image.open("play.png")
llevar_muestra_icon = llevar_muestra_image.resize((50, 50))
llevar_muestra_icon_tk = ImageTk.PhotoImage(llevar_muestra_icon)
btn_guardar = tk.Button(root, image=llevar_muestra_icon_tk, command=update_mosaico_muestra, bg="#7BC67B")
btn_guardar.place(x=820, y=40)

clear_image = Image.open("clear.png")
clear_icon = clear_image.resize((20, 20))
clear_icon_tk = ImageTk.PhotoImage(clear_icon)
btn_clear = tk.Button(root, image=clear_icon_tk, command=clear, bg="#7BC67B")
btn_clear.place(x=80, y=40)

constructor_image = Image.open("constructor.png")
constructor_icon = constructor_image.resize((50, 50))
constructor_icon_tk = ImageTk.PhotoImage(constructor_icon)
btn_constructor = tk.Button(root, image=constructor_icon_tk, command=construir, bg="#7BC67B")
btn_constructor.place(x=20, y=480)

mosaico_muestra = tk.Canvas(root, width=can_width*pixel_size, height=can_height*pixel_size, highlightthickness=0)
mosaico_muestra.place(x=900, y=40)
celdas = [[None for _ in range(can_height)] for _ in range(can_width)]
celdas2 = [[None for _ in range(can_height)] for _ in range(can_width)]

label_tools = tk.Label(root, text="Tools", bg="#5C5C8C", font=("Arial", 12))
label_tools.place(x=20, y=10)

label_canvas1 = tk.Label(root, text="Background", bg="#5C5C8C", font=("Arial", 12))
label_canvas1.place(x=140, y=10)

label_canvas2 = tk.Label(root, text="Texture & Border", bg="#5C5C8C", font=("Arial", 12))
label_canvas2.place(x=480, y=10)

for i in range(can_width):
	for j in range(can_height):
		canvas = tk.Canvas(root, width=pixel_size, height=pixel_size, highlightthickness=0)
		canvas.place(x=(i+7)*pixel_size, y=(j+2)*pixel_size)
		canvas.bind("<Button-1>", draw)
		canvas.bind("<B1-Motion>", start_draw)
		canvas.bind("<ButtonRelease-1>", end_draw)
		celdas[i][j] = canvas

for i in range(can_width):
	for j in range(can_height):
		canvas = tk.Canvas(root, width=pixel_size, height=pixel_size, highlightthickness=0)
		canvas.place(x=(i+24)*pixel_size, y=(j+2)*pixel_size)
		canvas.bind("<Button-1>", draw)
		canvas.bind("<B1-Motion>", start_draw)
		canvas.bind("<ButtonRelease-1>", end_draw)
		celdas2[i][j] = canvas

label_constructor = tk.Label(root, text="Blob", bg="#5C5C8C", font=("Arial", 12))
label_constructor.place(x=140, y=370)

constructor = tk.Label(root, width=480, height=240, bg="#5C5C8C")
constructor.place(x=140, y=400)

root.mainloop()