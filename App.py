import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import kernels
import math
import colorsys

Gx = [[-1, 0, 1],
      [-2, 0, 2],
      [-1, 0, 1]]
Gy = [[1, 2, 1],
      [0, 0, 0],
      [-1, -2, -1]]


def ConvolveRGB(img, kernel):
    WIDTH, HEIGHT = img.size
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


def ConvolveL(img, kernel):
    WIDTH, HEIGHT = img.size
    new_img = Image.new(mode="L", size=(WIDTH, HEIGHT))
    new_pixel_map = new_img.load()
    for x in range(WIDTH):
        for y in range(HEIGHT):
            acc = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT:
                        acc += kernel[dx + 1][dy + 1] * img.getpixel((x + dx, y + dy))
            new_pixel_map[x, y] = int(acc)
    return new_img


def new_img(img, mode="L"):
    new_img = Image.new(mode=mode, size=img.size)
    return new_img


def intensity(img):
    WIDTH, HEIGHT = img.size
    intensity = new_img(img)
    intensity_map = intensity.load()
    for x in range(WIDTH):
        for y in range(HEIGHT):
            R, G, B, A = img.getpixel((x, y))
            GRAYSCALE = sum((0.2126 * R, 0.7152 * G, 0.0722 * B))
            intensity_map[x, y] = int(GRAYSCALE)
    return intensity


def sobel_edge(img):
    WIDTH, HEIGHT = img.size
    edge = new_img(img)
    edge_map = edge.load()
    gradient_direction = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for x in range(WIDTH):
        for y in range(HEIGHT):
            GxA = 0
            GyA = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT:
                        GxA += Gx[dx + 1][dy + 1] * img.getpixel((x + dx, y + dy))
                        GyA += Gy[dx + 1][dy + 1] * img.getpixel((x + dx, y + dy))
            gradient_direction[y][x] = math.atan2(GyA, GxA)
            G = math.sqrt(GxA ** 2 + GyA ** 2)
            edge_map[x, y] = int(min(max(G, 0), 255))
    return edge, gradient_direction


def sobel_gradient(edge, gradient_direction):
    WIDTH, HEIGHT = edge.size
    edge_map = edge.load()
    gradient = new_img(edge, "RGB")
    gradient_map = gradient.load()

    for x in range(WIDTH):
        for y in range(HEIGHT):
            if gradient_direction[y][x] != 0 and edge_map[x, y] > 100:

                direction_normalized = (gradient_direction[y][x] + math.pi) / (2 * math.pi)

                hue = direction_normalized
                saturation = 1.0
                value = 1.0

                r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)

                gradient_map[x, y] = (int(r * 255), int(g * 255), int(b * 255))

    return gradient


BACKGROUND_COLOR = "#2E2E2E"
FOREGROUND_COLOR = "#F5F5F5"
BUTTON_COLOR = "#444444"
BUTTON_TEXT_COLOR = "#F5F5F5"
HIGHLIGHT_COLOR = "#616161"


class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Filter Application")

        self.root.configure(bg=BACKGROUND_COLOR)

        self.image = None
        self.filtered_image = None

        self.canvas = tk.Canvas(root, width=500, height=500, bg=BACKGROUND_COLOR, highlightbackground=HIGHLIGHT_COLOR)
        self.canvas.grid(row=0, column=0, rowspan=10, padx=10, pady=10)

        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
        self.upload_button.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

        self.reset_button = tk.Button(root, text="Reset Image", command=self.reset_image, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
        self.reset_button.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

        self.sobel_button = tk.Button(root, text="Apply Sobel", command=self.apply_sobel, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
        self.sobel_button.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

        self.sobel_button_gradient = tk.Button(root, text="Apply Sobel Gradient", command=self.apply_sobel_gradient, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
        self.sobel_button_gradient.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

        self.kernel_label = tk.Label(root, text="Choose Convolutions:", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
        self.kernel_label.grid(row=4, column=1, padx=10, pady=5, sticky='w')

        self.kernel_vars = {}

        kernel_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        kernel_frame.grid(row=5, column=1, padx=10, pady=5, sticky='ew')

        row_count = 0
        for kernel_name in dir(kernels):
            if not kernel_name.startswith("__"):
                var = tk.IntVar()
                chk = tk.Checkbutton(kernel_frame, text=kernel_name, variable=var, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, selectcolor=HIGHLIGHT_COLOR, activebackground=BUTTON_COLOR)
                chk.grid(row=row_count, column=0, padx=5, pady=2, sticky='w')  # Add padding for spacing
                self.kernel_vars[kernel_name] = var
                row_count += 1

        self.apply_button = tk.Button(root, text="Apply Convolution", command=self.apply_convolution, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
        self.apply_button.grid(row=6, column=1, padx=10, pady=10, sticky='ew')

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path).convert("RGBA")
            self.orig_image = Image.open(file_path).convert("RGBA")
            self.display_image(self.image)

    def reset_image(self):
        img_resized = self.orig_image.resize((500, 500))
        self.tk_image = ImageTk.PhotoImage(img_resized)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

    def display_image(self, image):
        img_resized = image.resize((500, 500))
        self.tk_image = ImageTk.PhotoImage(img_resized)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

    def apply_sobel(self):
        if self.orig_image:
            self.image = intensity(self.orig_image)
            self.filtered_image = sobel_edge(self.image)[0]
            self.display_image(self.filtered_image)

    def apply_sobel_gradient(self):
        if self.orig_image:
            self.image = intensity(self.orig_image)
            self.filtered_image = sobel_gradient(*sobel_edge(self.image))
            self.display_image(self.filtered_image)

    def apply_convolution(self):
        if self.orig_image:
            self.filtered_image = self.orig_image
            flag1 = False
            flag2 = False
            for kernel_name, var in self.kernel_vars.items():
                if var.get() == 1:
                    kernel = getattr(kernels, kernel_name)
                    if kernel_name not in ["gaussian", "blur"]:
                        flag1 = True
                    if flag1:
                        if not flag2:
                            flag2 = True
                            self.filtered_image = intensity(self.filtered_image)
                        self.filtered_image = ConvolveL(self.filtered_image, kernel)
                    else:
                        self.filtered_image = ConvolveRGB(self.filtered_image, kernel)

            self.display_image(self.filtered_image)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageFilterApp(root)
    root.mainloop()
