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
        print(guitar.int_to_note(n[1]) + "\tat fret " + str(n[2]) + " on " + guitar.tunning[n[0]] + " string")


# BMP rendering stuff
font_file = open("font.bmp", "rb")
dib_head = bmp.read_dib_head(font_file)
bmp_head = bmp.read_bmp_head(font_file)

font_height = dib_head["BMP_HEIGHT"]
font_width = dib_head["BMP_WIDTH"]
amt_of_pixles = int(dib_head["RAW_IMG_SIZE"] / (dib_head["BITS_PER_PIX"] / 8.0))

font_file.seek(bmp_head["IMG_DATA_START_ADDR"])
img_data = []
for i in range(amt_of_pixles):
        img_data.append(bmp.read_pix(font_file))
font_file.close()
# flip horz
img_data.reverse()
# flip vert
img_data_tmp = []
for y in range(font_height):
    for x in range(font_width):
        pix = img_data[(y * (font_width + 1)) + (font_width - x)]
        img_data_tmp.append(pix)
img_data = img_data_tmp

def get_bmp_char(c):
    offset_in_font_file = ord(c) - ord(' ')
    cx = offset_in_font_file % 10
    cy = int(offset_in_font_file / 10)
    bmp_char = []
    # length of side of square that contains a single character
    bmp_char_size = 26
    for y in range(bmp_char_size):
        for x in range(bmp_char_size):
            pix = img_data[((y + cy * (bmp_char_size - 1)) * font_width) + (x + cx * (bmp_char_size - 1))]
            bmp_char.append(pix)
    return bmp_char

def draw_text(x_pos, y_pos, text, img, fill_bg=False, color=[255, 0, 0], bg_color=[0, 0, 0], width=26):
    # draw text with bmp font
    xoffset = 0
    for c in text:
        bmp_char = get_bmp_char(c)
        for y in range(26):
            for x in range(width):
                pix = bmp_char[(y * 26) + x]
                if (pix[0] + pix[1] + pix[2] == 255 * 3):
                    img.write_pix(x + x_pos + xoffset, y + y_pos, color[0], color[1], color[2])
                elif fill_bg:
                    img.write_pix(x + x_pos + xoffset, y + y_pos, bg_color[0], bg_color[1], bg_color[2])
        xoffset += width

width = 1000
height = 400
# draw background
img_out = bmp_image("test.bmp", width, height)
for x in range(width):
    for y in range(height):
        img_out.write_pix(x, y, 25, 25, 25)

def render_triad(x_pos, y_pos, chord_type, note):
    chord = guitar.chord_types[chord_type](note)
    freted_chord = guitar.find_triad_lin_scan(chord, 0)
    yoffset = 50
    # draw strings
    for string in range(len(guitar.tunning)):
        thickness = 3
        for x in range(20, 970):
            for y in range(thickness):
                img_out.write_pix(x_pos + x, y_pos + (string * 50) + yoffset + y, 0, 255, 0)
        x_offset = 0
        for fret in range(13):
            draw_text(x_pos + 30 + x_offset, y_pos + (string * 50) + (yoffset - 10), str(fret), img_out, True, width=13, bg_color=[25, 25, 25], color=[255, 255, 255])
            for n in freted_chord:
                if n[0] == string and n[2] == fret:
                    draw_text(x_pos + 30 + x_offset, y_pos + (string * 50) + (yoffset - 10), str(fret), img_out, True, width=13, bg_color=[25, 25, 25])
            x_offset += 75
    draw_text(x_pos + 20, y_pos, note + " " + chord_type, img_out, True, bg_color=[25, 25, 25], width=13)

render_triad(0, 0, "maj", "C")

img_out.write_img()

print("done.")
