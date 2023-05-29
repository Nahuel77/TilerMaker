import imports

def construir(can_width, can_height, celdas, celdas2, constructor_mark):
	#creo una imagen RGBA png para el canvas 1 y 2
	background = imports.Image.new("RGBA", ((can_width), (can_height)), (0, 0, 0, 0))
	details = imports.Image.new("RGBA", ((can_width), (can_height)), (0, 0, 0, 0))
	drawmap = imports.ImageDraw.Draw(background)
	drawmap2 = imports.ImageDraw.Draw(details)
	corner_one = imports.Image.new("RGBA", (32, 32), (0, 0, 0, 0))                 # ╔<<<
	corner_two = imports.Image.new("RGBA", (32, 32), (0, 0, 0, 0))             # ╝<<<
	corner_one_long = imports.Image.new("RGBA", (32, 32), (0, 0, 0, 0))            #╝╝╝╝<
	corner_four_long = imports.Image.new("RGBA", (32, 32), (0, 0, 0, 0))
	center = imports.Image.new("RGBA", (32, 32), (0, 0, 0, 0))
	draw_corner_one = imports.ImageDraw.Draw(corner_one)
	draw_corner_two = imports.ImageDraw.Draw(corner_two)
	draw_corner_one_long = imports.ImageDraw.Draw(corner_one_long)
	draw_corner_four_long = imports.ImageDraw.Draw(corner_four_long)
	draw_center = imports.ImageDraw.Draw(center)
	for i in range(can_width):
		for j in range(can_height):
			celda1 = celdas[i][j]
			celda2 = celdas2[i][j]
			color1 = celda1["background"]
			color2 = celda2["background"]
			if not(color1=="SystemButtonFace"):
				drawmap.rectangle(((i, j), ((i), (j))), fill=color1)
			if not(color2=="SystemButtonFace"):
				drawmap2.rectangle(((i, j), ((i), (j))), fill=color2)
				if ((j<16 and i>16) and (i+j)>=31):
					draw_corner_one.rectangle(((i, j), (i, j)), fill=color2)
				if ((i<16 and j<16) and (i-j)<=0):
					draw_corner_two.rectangle(((i, j), (i, j)), fill=color2)
				if (i>j):
					draw_corner_one_long.rectangle(((i, j), (i, j)), fill=color2)
				if (i+j)<=31:
					draw_corner_four_long.rectangle(((i, j), (i, j)), fill=color2)
				if (i>j) and ((i+j)<=31):
					draw_center.rectangle(((i, j), (i, j)), fill=color2)

	details.save("./details_tile.png", "PNG")
	corner_one.save("./corner_one.png", "PNG")
	corner_two.save("./corner_two.png", "PNG")
	corner_one_long.save("./corner_one_long.png", "PNG")
	corner_four_long.save("./corner_four_long.png", "PNG")
	center.save("./center.png", "PNG")

	#repito el canvas uno en forma de mosaicos 11x5
	tiles_set = imports.Image.new("RGBA", (can_width*11, can_height*5), (0, 0, 0, 0))

	for i in range(11):
		for j in range(5):
			tiles_set.paste(background, (i*can_width, j*can_height))

	mask = imports.Image.open("mask.png")
	mask = mask.convert("L")
	output = imports.ImageOps.fit(tiles_set, mask.size)
	output = output.convert("RGBA")
	output.putalpha(mask)

	output.save("./background_tile.png", "PNG")

	#repito los detalles para los tiles en top
	for i in range(11):
		for j in range(5):
			if ((i==1) or (i==5) or (i==6) or (i==8)) and (((j==0) or (j==3) and (i==1))):
				output.paste(details, (i*can_width, j*can_height), mask=details)

	for i in range(11):
		for j in range(5):
			if ((i==0 or i==4) and j==0) or (j==3 and i==0):
				output.paste(corner_one_long, (i*can_width, j*can_height), mask=corner_one_long)

	for i in range(11):
		for j in range(5):
			if ((i==2 or i==7) and j==0) or (j==3 and i==2):
				output.paste(corner_four_long, (i*can_width, j*can_height), mask=corner_four_long)

	for i in range(11):
		for j in range(5):
			if (j==0 or j==3) and (i==3):
				output.paste(center, (i*can_width, j*can_height), mask=center)

	for i in range (11):
		for j in range(5):
			if ((j==2 or j==3 or j==4) and (i==4 or i==5 or i==8)) or \
			((i==9 and (j==0 or j==2)) or (i==10 and (j==2 or j==3))):
				output.paste(corner_one, (i*can_width, j*can_height), mask=corner_one)

	for i in range(11):
		for j in range(5):
			if ((i==6 or i==7 or i==8) and (j==2 or j==3 or j==4)) or \
			((i==9 and (j==1 or j==2 or j==3)) or (i==10 and j==2)):
				output.paste(corner_two, (i*can_width, j*can_height), mask=corner_two)

	output.save("./background_tile.png", "PNG")
	#repito los detalles para los tiles en bottom
	details_botton = details.rotate(-180)
	for i in range(11):
		for j in range(5):
			if ((i==1) and (j==2)) or ((j==3) and ((i==1) or (i==5) or (i==6) or (i==8))):
				output.paste(details_botton, (i*can_width, j*can_height), mask=details_botton)

	corner_one_long_bottom = corner_one_long.rotate(-180)
	for i in range(11):
		for j in range(5):
			if (i==2 and (j==2 or j==3)) or (j==3 and i==7):
				output.paste(corner_one_long_bottom, (i*can_width, j*can_height), mask=corner_one_long_bottom)

	corner_four_long_bottom = corner_four_long.rotate(-180)
	for i in range(11):
		for j in range(5):
			if (i==0 and (j==2 or j==3)) or (i==4 and j==3):
				output.paste(corner_four_long_bottom, (i*can_width, j*can_height), mask=corner_four_long_bottom)

	center_bottom = center.rotate(-180)
	for i in range(11):
		for j in range(5):
			if (i==3 and (j==2 or j==3)):
				output.paste(center_bottom, (i*can_width, j*can_height), mask=center_bottom)

	corner_one_bottom = corner_one.rotate(-180)
	for i in range(11):
		for j in range(5):
			if (j==0 and (i==6 or i==7 or i==8 or i==9)) or \
			(j==1 and (i==6 or i==7 or i==8)) or (j==3 and (i==9 or i==10)) or \
			(j==4 and (i==6 or i==7 or i==8)) or (j==2 and i==9):
				output.paste(corner_one_bottom, (i*can_width, j*can_height), mask=corner_one_bottom)

	corner_two_bottom = corner_two.rotate(-180)
	for i in range(11):
		for j in range(5):
			if (i==4 and (j==0 or j==1 or j==4)) or \
			(i==5 and (j==0 or j==1 or j==4)) or \
			(i==8 and (j==0 or j==1 or j==4)) or \
			(i==9 and (j==1 or j==3)) or (i==10 and (j==2 or j==3)):
				output.paste(corner_two_bottom, (i*can_width, j*can_height), mask=corner_two_bottom)				

	output.save("./background_tile.png", "PNG")
	#repito los detalles para los tiles izquierdos
	details_left = details.rotate(90)
	for i in range(11):
		for j in range(5):
			if ((j==1) and ((i==0) or (i==3))) or ((i==4) and ((j==1) or (j==2) or (j==4))):
				output.paste(details_left, (i*can_width, j*can_height), mask=details_left)

	corner_one_long_left = corner_one_long.rotate(90)
	for i in range(11):
		for j in range(5):
			if ((j==2) and (i==0 or i==3)) or (i==4 and j==3):
				output.paste(corner_one_long_left, (i*can_width, j*can_height), mask=corner_one_long_left)

	corner_four_long_left = corner_four_long.rotate(90)
	for i in range(11):
		for j in range(5):
			if (j==0 and (i==0 or i==3 or i==4)):
				output.paste(corner_four_long_left, (i*can_width, j*can_height), mask=corner_four_long_left)

	center_left = center.rotate(90)
	for i in range(11):
		for j in range(5):
			if (j==3 and (i==0 or i==3)):
				output.paste(center_left, (i*can_width, j*can_height), mask=center_left)

	corner_one_left = corner_one.rotate(-90)
	for i in range(11):
		for j in range(5):
			if (i==4 and (j==0 or j==1 or j==4)) or \
			(i==5 and (j==0 or j==1 or j==4)) or \
			(i==8 and (j==0 or j==1 or j==4)) or \
			(i==9 and (j==1 or j==3)) or \
			(i==10 and (j==2 or j==3)):
				output.paste(corner_one_left, (i*can_width, j*can_height), mask=corner_one_left)

	corner_two_left = corner_two.rotate(-90)
	for i in range(11):
		for j in range(5):
			if (i==4 and (j==2 or j==3 or j==4)) or \
			(i==5 and (j==2 or j==3 or j==4)) or \
			(i==8 and (j==2 or j==3 or j==4)) or \
			(i==9 and (j==0 or j==2)) or (i==10 and (j==2 or j==3)):
				output.paste(corner_two_left, (i*can_width, j*can_height), mask=corner_two_left)

	output.save("./background_tile.png", "PNG")
	#repito los detalles para los tiles derechos
	details_right = details.rotate(-90)
	for i in range(11):
		for j in range(5):
			if ((j==1) and ((i==2) or (i==3))) or ((i==7) and ((j==1) or (j==2) or (j==4))):
				output.paste(details_right, (i*can_width, j*can_height), mask=details_right)

	corner_one_long_right = corner_one_long.rotate(-90)
	for i in range(11):
		for j in range(5):
			if (j==0 and (i==2 or i==3 or i==7)):
				output.paste(corner_one_long_right, (i*can_width, j*can_height), mask=corner_one_long_right)

	corner_four_long_right = corner_four_long.rotate(-90)
	for i in range(11):
		for j in range(5):
			if (j==2 and (i==2 or i==3)) or (j==3 and i==7):
				output.paste(corner_four_long_right, (i*can_width, j*can_height), mask=corner_four_long_right)

	center_right = center.rotate(-90)
	for i in range(11):
		for j in range(5):
			if (j==3 and (i==2 or i==3)):
				output.paste(center_right, (i*can_width, j*can_height), mask=center_right)

	corner_one_right = corner_one.rotate(90)
	for i in range(11):
		for j in range(5):
			if (i==6 and (j==2 or j==3 or j==4)) or \
			(i==7 and (j==2 or j==3 or j==4)) or \
			(i==8 and (j==2 or j==3 or j==4)) or \
			(i==9 and (j==1 or j==2 or j==3)) or (i==10 and j==2):
				output.paste(corner_one_right, (i*can_width, j*can_height), mask=corner_one_right)

	corner_two_right = corner_two.rotate(90)
	for i in range(11):
		for j in range(5):
			if (i==6 and (j==0 or j==1 or j==4)) or \
			(i==7 and (j==0 or j==1 or j==4)) or \
			(i==8 and (j==0 or j==1 or j==4)) or \
			(i==9 and (j==0 or j== 2 or j==3)) or (i==10 and j==3):
				output.paste(corner_two_right, (i*can_width, j*can_height), mask=corner_two_right)

	output.save("./background_tile.png", "PNG")

	tiles_set_tk = imports.ImageTk.PhotoImage(output)
	constructor_mark.configure(image=tiles_set_tk)
	constructor_mark.image = tiles_set_tk