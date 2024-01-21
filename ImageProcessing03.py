from PIL import Image

import kernels

image = Image.open(r"C:\Users\user\Downloads\sample_image.png")


def Convolve(img, kernel):
    HEIGHT, WIDTH = img.size
    new_img = Image.new(mode="RGBA", size=(WIDTH, HEIGHT))
    new_pixel_map = new_img.load()
    for x in range(WIDTH):
        for y in range(HEIGHT):
            acc_R = 0
            acc_G = 0
            acc_B = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT:
                        R, G, B, A = img.getpixel((x + dx, y + dy))
                        acc_R += kernel[dx + 1][dy + 1] * R
                        acc_G += kernel[dx + 1][dy + 1] * G
                        acc_B += kernel[dx + 1][dy + 1] * B
            new_pixel_map[x, y] = (int(acc_R), int(acc_G), int(acc_B))
    return new_img


def Grayscale(img):
    HEIGHT, WIDTH = img.size
    new_img = Image.new(mode="RGBA", size=(WIDTH, HEIGHT))
    new_pixel_map = new_img.load()
    for x in range(WIDTH):
        for y in range(HEIGHT):
            R, G, B, A = img.getpixel((x, y))
            grayscale = 0.299*R + 0.587*G + 0.114*B
            new_pixel_map[x, y] = (int(grayscale), int(grayscale), int(grayscale))
    return new_img


new_image = Convolve(Grayscale(image), kernels.edge)
new_image.show()
new_image = Convolve(Grayscale(image), kernels.emboss3)
new_image.show()
new_image = Convolve(Convolve(image, kernels.gaussian), kernels.edge)
