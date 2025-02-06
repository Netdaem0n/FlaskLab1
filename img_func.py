from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os

def img_info(file):
    if os.path.exists(file):
        with Image.open(file) as img:
            img_type = img.format
            img_size = img.size
            img_color = img.mode
        return img_type, img_size, img_color
    return None, None, None

def plot_img_color(file, fileout):
    if os.path.exists(file):
        with Image.open(file) as img:
            data = img.histogram()
            plt.figure(figsize=(10, 5))
            plt.title("Распределение цветов")
            plt.xlabel("Значение пикселя")
            plt.ylabel("Частота")
            colors = ('r', 'g', 'b')
            for i, color in enumerate(colors):
                plt.plot(data[i*256:(i+1)*256], color=color)
            plt.savefig(fileout)
            plt.close()
    return None

def transform_image(file, func, period, direction):
    if os.path.exists(file):
        with Image.open(file) as img:
            img = img.convert("RGB")
            data = np.array(img)
            height, width, _ = data.shape

            if func == "sin":
                func = np.sin
            else:
                func = np.cos

            if direction == 'horizontal':
                for y in range(height):
                    for x in range(width):
                        factor = (func(2 * np.pi * x / period) + 1) / 2
                        data[y, x] = np.clip(data[y, x] * factor, 0, 255)

            elif direction == 'vertical':
                for y in range(height):
                    for x in range(width):
                        factor = (func(2 * np.pi * y / period) + 1) / 2
                        data[y, x] = np.clip(data[y, x] * factor, 0, 255)

        transformed_img = Image.fromarray(data.astype('uint8'))
        file = file.replace('.', '_transformed.')
        transformed_img.save(file)
        return file
    return None

if __name__ == "__main__":
    file = r"C:\Temp_work\FlaskProject3\static\images\userfiles\0e4339a1-422e-4d4e-abc4-02374b41bd0f.png"
    data = img_info(file)
    plot_img_color(file, "plot.png")
    transform_image(file, "sin", 10, "horizontal")