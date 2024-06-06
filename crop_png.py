# 裁剪1024*1024的png为256*256   开发时间：2023/5/9 10:45


import os

from PIL import Image


def crop_image(image_path, output_path, crop_size, code):
    with Image.open(image_path) as img:
        width, height = img.size
        for i in range(0, width, crop_size):
            for j in range(0, height, crop_size):
                box = (i, j, i + crop_size, j + crop_size)
                cropped_img = img.crop(box)
                cropped_img.save(os.path.join(output_path, code+f"{i}_{j}.png"))
                print(code, f"{i}_{j}.png")


image_path = "label"
output_path = "LAB"
if not os.path.exists(output_path):
    os.makedirs(output_path)
crop_size = 256

count = 0

for filename in os.listdir(image_path):
    if filename.endswith(".png"):
        count += 1
        code = f'{count:05d}'
        image_file = os.path.join(image_path, filename)
        crop_image(image_file, output_path, crop_size, code)
