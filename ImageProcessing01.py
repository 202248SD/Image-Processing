from PIL import Image
import kernels

img = Image.open(r"C:\Users\user\Downloads\sample_image.png")
HEIGHT, WIDTH = img.size
pixel_map = img.load()
kernel = kernels.edge

new_img = Image.new(mode="RGBA", size=(WIDTH, HEIGHT))
new_pixel_map = new_img.load()
for x in range(WIDTH):
    for y in range(HEIGHT):
        acc_R = 0
        acc_G = 0
        acc_B = 0
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT:
                    R, G, B, A = img.getpixel((x + dx, y + dy))
                    acc_R += kernel[dx + 1][dy + 1] * R
                    acc_G += kernel[dx + 1][dy + 1] * G
                    acc_B += kernel[dx + 1][dy + 1] * B
        new_pixel_map[x, y] = (acc_R, acc_G, acc_B)

new_img.show()
