from PIL import Image
import os
import numpy as np

def apply_grayscale_filter(image_path, output_dir=".", output_filename="grayscale_image.jpg"):
    """
    给图像应用灰度滤镜，并保存到指定目录

    参数:
    - image_path: 输入图像的路径
    - output_dir: 输出目录，默认为当前目录
    - output_filename: 输出文件名，默认为 'grayscale_image.jpg'

    返回:
    - 返回转化后的灰度图像
    """
    # 检查输出目录是否存在，如果不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 打开图像并转换为 numpy 数组
    image = Image.open(image_path)
    img_array = np.array(image)

    # 使用加权平均方法直接通过 NumPy 转换为灰度图
    # 灰度值公式：0.2989 * R + 0.5870 * G + 0.1140 * B
    grayscale_array = 0.2989 * img_array[:, :, 0] + 0.5870 * img_array[:, :, 1] + 0.1140 * img_array[:, :, 2]

    # 将灰度数组转回图像
    grayscale_image = Image.fromarray(np.uint8(grayscale_array))

    # 生成保存路径
    output_path = os.path.join(output_dir, output_filename)

    # 保存灰度图像到指定目录
    grayscale_image.save(output_path)
    print(f"灰度图像已保存为: {output_path}")

    return grayscale_image


# 示例用法
image_path = 'D:/深度学习实践/dog.jpg'  # 替换为你自己的图像路径
output_dir = 'D:/深度学习实践/output'  # 指定输出目录
filtered_img = apply_grayscale_filter(image_path, output_dir)

