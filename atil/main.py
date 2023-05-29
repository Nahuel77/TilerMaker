import imports

############################################################################################################
#            Astor Tiler - Desarrollado por Nahuel. nahuelastor@gmail.com           2023                   #
############################################################################################################

root = imports.tk.Tk()
root.geometry("800x600+50+50")
root.config(bg="#5C5C8C")
root.wm_state('zoomed')
root.resizable(False, False)
color = "#000000"

can_width = 32
can_height = 32
pixel_size = 10
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
			while pressed and isinstance(widget, imports.tk.Canvas):
				widget.configure(bg=color)
				end_draw(event)
		elif fill_status:
			if color_anterior == color:
				return
			queue = imports.Q.Queue()
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
			while pressed and isinstance(widget, imports.tk.Canvas):
				widget.configure(bg="SystemButtonFace")
				end_draw(event)
		else:
			color = color_anterior
			if (color!="SystemButtonFace"):
				frame.config(bg=color)
				label_clean.place_forget()
			elif (color=="SystemButtonFace"):
				label_clean.place(x=51, y=71)
			root.config(cursor="arrow")
			draw_status = True

def cancel_tool(event):
	pass

def seleccion_color():
	global color
	picked_color = imports.colorchooser.askcolor()
	color = picked_color[1]
	label_clean.place_forget()
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
			canvas_muestra = imports.tk.Canvas(mosaico_muestra, width=pixel_size, height=pixel_size, bg=color1, highlightthickness=0)
			canvas_muestra.place(x=i*pixel_size, y=j*pixel_size)
			if color2 != "SystemButtonFace":
				canvas2_muestra = imports.tk.Canvas(mosaico_muestra, width=pixel_size, height=pixel_size, bg=color2, highlightthickness=0)
				canvas2_muestra.place(x=i*pixel_size, y=j*pixel_size)

############################################################################################################

def call_constructor():
	imports.constructor.construir(can_width, can_height, celdas, celdas2, constructor_mark)

############################################################################################################

pen_image = imports.Image.open("pen.png")
pen_icon = pen_image.resize((20, 20))
pen_icon_tk = imports.ImageTk.PhotoImage(pen_icon)
btn_pen = imports.tk.Button(root, image=pen_icon_tk, command=pen, bg="#7BC67B")
btn_pen.place(x=20, y=40)

color_imagen = imports.Image.open("paleta.png")
color_icon = color_imagen.resize((20, 20))
color_icon_tk = imports.ImageTk.PhotoImage(color_icon)
btn_color = imports.tk.Button(root, image=color_icon_tk, command=seleccion_color, bg="#7BC67B")
btn_color.place(x=20, y=70)

fill_image = imports.Image.open("fill.png")
fill_icon = fill_image.resize((20, 20))
fill_icon_tk = imports.ImageTk.PhotoImage(fill_icon)
btn_fill = imports.tk.Button(root, image=fill_icon_tk, command=fill, bg="#7BC67B")
btn_fill.place(x=50, y=40)

eyerdropper_image = imports.Image.open("gotero.png")
eyerdropper_icon = eyerdropper_image.resize((20, 20))
eyerdropper_icon_tk = imports.ImageTk.PhotoImage(eyerdropper_icon)
btn_eyerdropper = imports.tk.Button(root, image=eyerdropper_icon_tk, command=eyerdropper, bg="#7BC67B")
btn_eyerdropper.place(x=80, y=70)

frame = imports.tk.Frame(root, bg=color, width=26, height=26)
frame.place(x=50, y=70)

llevar_muestra_image = imports.Image.open("play.png")
llevar_muestra_icon = llevar_muestra_image.resize((50, 50))
llevar_muestra_icon_tk = imports.ImageTk.PhotoImage(llevar_muestra_icon)
btn_guardar = imports.tk.Button(root, image=llevar_muestra_icon_tk, command=update_mosaico_muestra, bg="#7BC67B")
btn_guardar.place(x=820, y=40)

clear_image = imports.Image.open("clear.png")
clear_icon = clear_image.resize((20, 20))
clear_icon_tk = imports.ImageTk.PhotoImage(clear_icon)
btn_clear = imports.tk.Button(root, image=clear_icon_tk, command=clear, bg="#7BC67B")
btn_clear.place(x=80, y=40)

constructor_image = imports.Image.open("constructor.png")
constructor_icon = constructor_image.resize((50, 50))
constructor_icon_tk = imports.ImageTk.PhotoImage(constructor_icon)
btn_constructor = imports.tk.Button(root, image=constructor_icon_tk, command=call_constructor, bg="#7BC67B")
btn_constructor.place(x=20, y=480)

mosaico_muestra = imports.tk.Canvas(root, width=can_width*pixel_size, height=can_height*pixel_size, highlightthickness=0)
mosaico_muestra.place(x=900, y=40)
celdas = [[None for _ in range(can_height)] for _ in range(can_width)]
celdas2 = [[None for _ in range(can_height)] for _ in range(can_width)]

label_tools = imports.tk.Label(root, text="Tools", bg="#5C5C8C", font=("Arial", 12))
label_tools.place(x=20, y=10)

label_canvas1 = imports.tk.Label(root, text="Background", bg="#5C5C8C", font=("Arial", 12))
label_canvas1.place(x=140, y=10)

label_canvas2 = imports.tk.Label(root, text="Texture & Border", bg="#5C5C8C", font=("Arial", 12))
label_canvas2.place(x=480, y=10)

for i in range(can_width):
	for j in range(can_height):
		canvas = imports.tk.Canvas(root, width=pixel_size, height=pixel_size, highlightthickness=0)
		canvas.place(x=(i+14)*pixel_size, y=(j+4)*pixel_size)
		canvas.bind("<Button-1>", draw)
		canvas.bind("<B1-Motion>", start_draw)
		canvas.bind("<ButtonRelease-1>", end_draw)
		celdas[i][j] = canvas

for i in range(can_width):
	for j in range(can_height):
		canvas = imports.tk.Canvas(root, width=pixel_size, height=pixel_size, highlightthickness=0)
		canvas.place(x=(i+48)*pixel_size, y=(j+4)*pixel_size)
		canvas.bind("<Button-1>", draw)
		canvas.bind("<B1-Motion>", start_draw)
		canvas.bind("<ButtonRelease-1>", end_draw)
		celdas2[i][j] = canvas

label_clean = imports.tk.Label(root, width=20, height=20, image=clear_icon_tk, bg="#5C5C8C")
label_clean.place_forget()

label_constructor = imports.tk.Label(root, text="Blob", bg="#5C5C8C", font=("Arial", 12))
label_constructor.place(x=140, y=370)

constructor_mark = imports.tk.Label(root, width=(can_width*11), height=(can_height*5), bg="#5C5C8C")
constructor_mark.place(x=140, y=400)

root.mainloop()