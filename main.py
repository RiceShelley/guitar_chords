#!/usr/bin/python3
import guitar
from bmp import bmp_image
import bmp


guitar.print_tunning()
#note = str(input("Enter root note: ")).upper()
note = "C"
c_type = "maj"

guitar.print_fret_board()

for i in range(4):
    print("staring at string " + str(i))
    print(guitar.chord_types[c_type](note))
    chord = guitar.chord_types[c_type](note)
    chord = guitar.find_triad_lin_scan(chord, i)
    print("")

    for n in chord:
        print(guitar.int_to_note(n[1]) + "\tat fret " + str(n[2]) + " on " + guitar.guitar_tunning[n[0]] + " string")

width = 1000
height = 500
img_out = bmp_image("test", width, height)
for x in range(width):
    for y in range(height):
        img_out.write_pix(x, y, 255, 255, 255)

thickness = 3
for x in range(20, 400):
    for y in range(thickness):
        img_out.write_pix(x, 100 + y, 0, 0, 0)
img_out.write_img()

font_file = open("font.bmp", "rb")
print(bmp.read_bmp_head(font_file))

print("done.")
