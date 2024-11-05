from PIL import Image
import numpy as np


def filter(img, intensity=0.5):
    image = img
    img_array = np.array(image)

    # 调整护眼模式的增强系数
    # 使用较为平滑的色彩增强方法，避免过于突兀的效果
    blue_channel = img_array[:, :, 0] * 0.7  # 轻微减少蓝色
    green_channel = img_array[:, :, 1] * (1 + 0.1 * intensity)  # 适当增强绿色
    red_channel = img_array[:, :, 2] * (1 + 0.2 * intensity)  # 更强烈地增强红色

    # 合并通道，确保像素值在 0-255 范围内
    np.clip(blue_channel, 0, 255, out=blue_channel)
    np.clip(green_channel, 0, 255, out=green_channel)
    np.clip(red_channel, 0, 255, out=red_channel)

    # 直接修改图像通道，而不是重新赋值整个数组
    img_array[:, :, 0] = blue_channel
    img_array[:, :, 1] = green_channel
    img_array[:, :, 2] = red_channel

    # 使用加权平均使图像色彩更平滑
    img_array = np.uint8(img_array * (1 - intensity) + np.array(image) * intensity)

    # 将处理后的数组转换回图像
    eye_care_image = Image.fromarray(img_array)

    return eye_care_image

