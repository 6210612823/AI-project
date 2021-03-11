from math import sqrt

from PIL import Image, ImageDraw


class ResizeImage:

    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.img = cv.imread(os.path.join(folder, filename))

    def resize(self):
        r = 255.0 / self.img.shape[1]
        dim = (255, int(self.img.shape[0] * r))
        # perform the actual resizing of the image and show it
        resized = cv.resize(self.img, dim, interpolation=cv.INTER_AREA)

        file = f"thumbnail.{self.filename[-3:]}"
        cv.imwrite(file, resized)
        shutil.move(f"{file}", f"{self.folder}/{self.filename}")


class DrawFakeRetina:
    kernely = [[-1, 0, 1],
               [-2, 0, 2],
               [-1, 0, 1]]
    kernelx = [[-1, -2, -1],
               [0, 0, 0],
               [1, 2, 1]]

    def __init__(self, filename):
        self.input_image = Image.open(filename)
        self.input_pixels = self.input_image.load()
        self.output_image = Image.new("RGB", self.input_image.size)

    def draw(self):
        draw = ImageDraw.Draw(self.output_image)
        for x in range(1, self.input_image.width - 1):
            for y in range(1, self.input_image.height - 1):
                magx, magy = 0, 0
                for a in range(3):
                    for b in range(3):
                        xn = x + a - 1
                        yn = y + b - 1
                        intensity = sum(self.input_pixels[xn, yn]) / 3
                        magx += intensity * self.kernelx[a][b]
                        magy += intensity * self.kernely[a][b]

                # Draw in black and white the magnitude
                color = int(sqrt(magx ** 2 + magy ** 2))
                draw.point((x, y), (color, color, color))
        self.output_image.save("1.png")
