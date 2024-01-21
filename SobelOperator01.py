from PIL import Image
import math

img = Image.open(r"C:\Users\user\Downloads\sample_image.png")

HEIGHT, WIDTH = img.size
intensity, blur, edge = Image.new(mode="L", size=(WIDTH, HEIGHT)), Image.new(mode="L", size=(WIDTH, HEIGHT)), Image.new(
    mode="L", size=(WIDTH, HEIGHT)),
intensity_map, blur_map, edge_map = intensity.load(), blur.load(), edge.load()
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
for x in range(WIDTH):
    for y in range(HEIGHT):
        GxA = 0
        GyA = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT:
                    GxA += Gx[dx + 1][dy + 1] * blur.getpixel((x + dx, y + dy))
                    GyA += Gy[dx + 1][dy + 1] * blur.getpixel((x + dx, y + dy))
        G = math.sqrt(GxA ** 2 + GyA ** 2)
        edge_map[x, y] = int(G)
edge.show()
