# number of cell rows
H = 14
# number of cell columns
W = 14

f = open('../input/14x14-1.ppm')

f.readline()
f.readline()
header = f.readline()

maxVal = f.readline()

w, h = map((int), header.split())

# initialize matrix
img = [0]*h
for i in range(h):
    img[i] = [0]*w
    for j in range(w):
        img[i][j] = [0]*3;

# read image
for i in range(h):
    for j in range(w):
        for k in range(3):
            img[i][j][k] = (int) (f.readline())

# cell height
cell_h = h / H
cell_w = w / W

def findInclude (pixel_color):
    for i, color in enumerate(colors):
        if color == pixel_color:
            return i
    colors.append(pixel_color)
    return len(colors) - 1

colors = []

print H, W
for i in range(H):
    for j in range(W):
        y = (int) ((i + 0.5) * cell_h)
        x = (int) ((j + 0.5) * cell_w)
        pixel_color = img[y][x]
        color = findInclude (pixel_color)
        #print pixel_color
        print '%5d' % (color),
    print ''

f.close()
