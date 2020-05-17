#!/usr/bin/python3
from math import sin

class bmp_image:
    def __init__(self, filename, width, height):
        self.filename = filename
        self.width = width
        self.height = height
        self.area = width * height
        print(self.area)
        self.pixles = [bytearray([0, 0, 0])] * self.area
        return
 
    def write_img(self):
        f = open(self.filename, "wb")
        f.write(self.create_bitmap_head(self.area + 14 + 40, 14 + 40))
        f.write(self.create_dib_head(self.width, self.height, self.area))
        for p in self.pixles:
            f.write(p)
        f.close() 
        return       

    def create_bitmap_head(self, raw_size, img_start_addr):
        bmp_head = bytearray(14)
        bmp_head[0:2] = "BM".encode()
        bmp_head[2:6] = int(raw_size).to_bytes(4, 'little')
        bmp_head[6:10] = int(0).to_bytes(4, 'little')
        bmp_head[10:] = int(img_start_addr).to_bytes(4, 'little')
        return bmp_head

    def create_dib_head(self, width, height, raw_size):
        dib_head = bytearray(40)
        dib_head[0:4] = int(40).to_bytes(4, 'little')
        dib_head[4:8] = int(width).to_bytes(4, 'little')
        dib_head[8:12] = int(height).to_bytes(4, 'little')
        dib_head[12:14] = int(1).to_bytes(2, 'little')
        dib_head[14:16] = int(24).to_bytes(2, 'little')
        dib_head[16:20] = int(0).to_bytes(4, 'little')
        dib_head[20:24] = int(raw_size).to_bytes(4, 'little')
        dib_head[24:28] = int(0).to_bytes(4, 'little')
        dib_head[28:32] = int(0).to_bytes(4, 'little')
        dib_head[28:32] = int(0).to_bytes(4, 'little')
        dib_head[32:34] = int(0).to_bytes(4, 'little')
        dib_head[34:38] = int(0).to_bytes(4, 'little')
        dib_head[38:] = int(0).to_bytes(2, 'little')
        return dib_head

    def write_pix(self, x, y, r, g, b):
        if (x > self.width - 1 or y > self.height - 1):
            return
        self.pixles[self.width * (self.height - y - 1) + x] = bytearray([b, g, r])
        return

def read_hex_img(filename):
        fhex = open(filename, "r")
        pix_ln = fhex.readlines();
        fhex.close()
        i = 0
        j = 0
        img_data = []
        img_data.append([0, 0, 0])
        for p in pix_ln:
            img_data[i][j] = int(p.strip('\n'), 16)
            j = j + 1
            if (j == 3):
                i = i + 1
                j = 0
                img_data.append([0, 0, 0])
        img_data.pop(-1)
        return img_data

def read_pix(f):
    pix = [0, 0, 0]
    pix[2] = int.from_bytes(f.read(1), byteorder='little', signed=False)
    pix[1] = int.from_bytes(f.read(1), byteorder='little', signed=False)
    pix[0] = int.from_bytes(f.read(1), byteorder='little', signed=False)
    return pix

def read_dib_head(f):
    print("<--- BMP DIB header info --->")
    f.seek(14)
    print("DIB header len = " + str(int.from_bytes(f.read(4), byteorder='little', signed=False)))
    print("bmp width = " + str(int.from_bytes(f.read(4), byteorder='little', signed=False)))
    print("bmp height = " + str(int.from_bytes(f.read(4), byteorder='little', signed=False)))
    print("color planes = " + str(int.from_bytes(f.read(2), byteorder='little', signed=False)))
    print("bits per pix = " + str(int.from_bytes(f.read(2), byteorder='little', signed=False)))
    print("compression method = " + str(int.from_bytes(f.read(4), byteorder='little', signed=False)))
    print("raw img size = " + str(int.from_bytes(f.read(4), byteorder='little', signed=False)))
    print("horizontal res (pix per metre) = " + str(int.from_bytes(f.read(4), byteorder='little', signed=True)))
    print("vertical res (pix per metre) = " + str(int.from_bytes(f.read(4), byteorder='little', signed=True)))
    print("number of colors = " + str(int.from_bytes(f.read(4), byteorder='little', signed=False)))
    print("number of important colors = " + str(int.from_bytes(f.read(4), byteorder='little', signed=False)))
    return 

def read_bmp_head(f):
    print("<--- BMP header info --->")
    f.seek(0)
    bmp_head = []
    if f.read(2).decode() != "BM":
        print("Invalid BMP header")
        return
    # BMP file size in bytes
    bmp_head.append(int.from_bytes(f.read(4), byteorder='little', signed=False))
    f.seek(10)
    # BMP img data start addr
    bmp_head.append(int.from_bytes(f.read(4), byteorder='little', signed=False))
    return bmp_head
