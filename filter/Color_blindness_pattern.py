from PIL import Image
import numpy as np


def filter(img):
    # 打开图像并转换为 numpy 数组
    image = img
    img_array = np.array(image)

    # 红绿色盲的转换矩阵（Deuteranopia）
    # 这个矩阵将会影响绿色和红色通道，模拟红绿色盲
    matrix = np.array([[0.625, 0.375, 0], [0.7, 0.3, 0], [0, 0.3, 0.7]])

    # 使用矩阵变换来模拟红绿色盲效果
    transformed_img_array = np.dot(img_array[..., :3], matrix.T)

    # 确保像素值在 0-255 范围内
    transformed_img_array = np.clip(transformed_img_array, 0, 255)

    # 将处理后的数组转换回图像
    red_green_blind_image = Image.fromarray(np.uint8(transformed_img_array))

    return red_green_blind_image
