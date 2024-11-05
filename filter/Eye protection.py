from PIL import Image
import numpy as np
import os

def apply_eye_care_filter(image_path, output_dir=".", output_filename="eye_care_image.jpg", intensity=0.5):
    """
    给图像应用护眼模式滤镜，并保存到指定目录
    通过加权融合，使图像效果更自然平滑。

    参数:
    - image_path: 输入图像的路径
    - output_dir: 输出目录，默认为当前目录
    - output_filename: 输出文件名，默认为 'eye_care_image.jpg'
    - intensity: 调整护眼效果的强度，0 表示不处理，1 表示完全处理

    返回:
    - 返回加上护眼滤镜的图像
    """
    # 检查输出目录是否存在，如果不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 打开图像并转换为 numpy 数组
    image = Image.open(image_path)
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

    # 生成保存路径
    output_path = os.path.join(output_dir, output_filename)

    # 保存处理后的图像
    eye_care_image.save(output_path)
    print(f"护眼模式图像已保存为: {output_path}")

    return eye_care_image

# 示例用法
image_path = 'D:/深度学习实践/dog.jpg'  # 替换为你自己的图像路径
output_dir = 'D:/深度学习实践/output'  # 指定输出目录
filtered_img = apply_eye_care_filter(image_path, output_dir, intensity=0.5)
