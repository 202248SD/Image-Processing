from PIL import Image
import math

img = Image.open(r"/Users/202248/Downloads/sample.png")

HEIGHT, WIDTH = img.size
intensity, blur, edge = Image.new(mode="L", size=(WIDTH, HEIGHT)), Image.new(mode="L", size=(WIDTH, HEIGHT)), Image.new(
    mode="L", size=(WIDTH, HEIGHT))
intensity_map, blur_map, edge_map = intensity.load(), blur.load(), edge.load()
gradient = Image.new(mode="RGB", size=(WIDTH, HEIGHT))
gradient_map = gradient.load()

Gx = [[-1, 0, 1],
      [-2, 0, 2],
      [-1, 0, 1]]
Gy = [[1, 2, 1],
      [0, 0, 0],
      [-1, -2, -1]]
gaussian = [[1 / 16, 1 / 8, 1 / 16],
            [1 / 8, 1 / 4, 1 / 8],
            [1 / 16, 1 / 8, 1 / 16]]
for x in range(WIDTH):
    for y in range(HEIGHT):
        R, G, B, A = img.getpixel((x, y))
        GRAYSCALE = sum((0.2126 * R, 0.7152 * G, 0.0722 * B))
        intensity_map[x, y] = int(GRAYSCALE)

for x in range(WIDTH):
    for y in range(HEIGHT):
        acc = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT:
                    acc += gaussian[dx + 1][dy + 1] * intensity.getpixel((x + dx, y + dy))
        blur_map[x, y] = int(acc)

arr = []
gradient_direction = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]
for x in range(WIDTH):
    for y in range(HEIGHT):
        GxA = 0
        GyA = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT:
                    GxA += Gx[dx + 1][dy + 1] * blur.getpixel((x + dx, y + dy))
                    GyA += Gy[dx + 1][dy + 1] * blur.getpixel((x + dx, y + dy))
        if GyA and GxA != 0:
            gradient_direction[x][y] = math.atan2(GyA, GxA)
        G = math.sqrt(GxA ** 2 + GyA ** 2)
        edge_map[x, y] = int(G)
edge.show()
for x in range(WIDTH):
    for y in range(HEIGHT):
        if gradient_direction[x][y] != 0 and edge_map[x, y] > 100:
            value = (255/math.pi)*(gradient_direction[x][y]+math.pi)
            print(value)
            gradient_map[x, y] = (int(max(255-value, 0)), int(min(value, 510-value)), int(min(max(0, value-255), 255)))
gradient.show()
