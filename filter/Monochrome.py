from PIL import Image
import numpy as np


def filter(img):
    image = img
    img_array = np.array(image)

    # 使用加权平均方法直接通过 NumPy 转换为灰度图
    # 灰度值公式：0.2989 * R + 0.5870 * G + 0.1140 * B
    grayscale_array = 0.2989 * img_array[:, :, 0] + 0.5870 * img_array[:, :, 1] + 0.1140 * img_array[:, :, 2]

    # 将灰度数组转回图像
    grayscale_image = Image.fromarray(np.uint8(grayscale_array))

    return grayscale_image

