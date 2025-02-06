import os
from PIL import Image, ImageDraw, ImageFont
from random import randint, choice
import subprocess


def file_image_numbers(n: int, size: tuple[int, int] =(100, 80),
                       flag: str ='file', filename: str ='output', img_dir: str = r'static images',
                       color: str ='black', removefile: bool =True) -> str | bool | None:

    current_path = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(os.path.join(current_path, *img_dir.split())):
        os.makedirs(os.path.join(current_path, *img_dir.split()))
    current_path = os.path.join(current_path, *img_dir.split(), f'{filename}.png')

    n = min(10, n)
    x, y = size
    if x < n * 50:
        x = 50 * n
    size = (x, y)

    numbers = [str(x) for x in range(10)]
    text_captcha = "".join([choice(numbers) for x in range(n)])

    img = Image.new('RGB', size, color)
    font = ImageFont.truetype('Minecraft.ttf', 50)
    draw = ImageDraw.Draw(img)

    start = 8
    fill_colors = ['black', 'red', 'blue', 'yellow', 'purple', 'orange', 'pink', 'brown', 'gray']
    for elem in text_captcha:
        visota = randint(5, 30)
        draw.text((start, visota), elem, font=font, fill=choice(fill_colors))
        start += randint(35, 55)


    img.save(f'{current_path}') if flag == 'file' else None

    if removefile:
        try:
            process = subprocess.Popen(
                ["python", "remove_after_use.py", current_path, '60'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        except Exception as e:
            print(e)

    return text_captcha, current_path



if __name__ == '__main__':
    data = file_image_numbers(111, color='#1f7f11', removefile=True)
    print(data)
