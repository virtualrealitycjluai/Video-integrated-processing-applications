from PIL import Image
import numpy as np
import os


def apply_red_green_blind_filter(image_path, output_dir=".", output_filename="red_green_blind_image.jpg"):
    """
    给图像应用红绿色盲滤镜，并保存到指定目录

    参数:
    - image_path: 输入图像的路径
    - output_dir: 输出目录，默认为当前目录
    - output_filename: 输出文件名，默认为 'red_green_blind_image.jpg'

    返回:
    - 返回模拟红绿色盲效果的图像
    """
    # 检查输出目录是否存在，如果不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 打开图像并转换为 numpy 数组
    image = Image.open(image_path)
    img_array = np.array(image)

    # 红绿色盲的转换矩阵（Deuteranopia）
    # 这个矩阵将会影响绿色和红色通道，模拟红绿色盲
    matrix = np.array([[0.625, 0.375, 0], [0.7, 0.3, 0], [0, 0.3, 0.7]])

    # 使用矩阵变换来模拟红绿色盲效果
    transformed_img_array = np.dot(img_array[..., :3], matrix.T)

    # 确保像素值在0-255范围内
    transformed_img_array = np.clip(transformed_img_array, 0, 255)

    # 将处理后的数组转换回图像
    red_green_blind_image = Image.fromarray(np.uint8(transformed_img_array))

    # 生成保存路径
    output_path = os.path.join(output_dir, output_filename)

    # 保存处理后的图像
    red_green_blind_image.save(output_path)
    print(f"红绿色盲模式图像已保存为: {output_path}")

    return red_green_blind_image


# 示例用法
image_path = 'D:/深度学习实践/dog.jpg'  # 替换为你自己的图像路径
output_dir = 'D:/深度学习实践/output'  # 指定输出目录
filtered_img = apply_red_green_blind_filter(image_path, output_dir)
