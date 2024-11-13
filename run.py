from GUI import GUI
import cv2
from filter import Monochrome, Eye_protection, Color_blindness_pattern
from env_bridge import env_distribute as ed
import os
import tempfile
import shutil
import time


def generate_unique_path(path):
    """
    检查路径是否已存在，若存在则添加时间戳确保唯一性。
    """
    if os.path.exists(path):
        base, ext = os.path.splitext(path)
        timestamp = int(time.time())
        path = f"{base}_{timestamp}{ext}"
    return path


def copy_files_from_cache_to_destination(cache_folder, destination_folder):
    # 检查缓存文件夹是否存在
    if not os.path.exists(cache_folder):
        print(f"缓存文件夹 {cache_folder} 不存在")
        return

    # 遍历缓存文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(cache_folder):
        for file in files:
            # 构建缓存文件的完整路径
            cache_file_path = os.path.join(root, file)

            # 构建目标文件的完整路径
            destination_file_path = os.path.join(destination_folder, file)

            # 复制文件到目标路径
            shutil.copy2(cache_file_path, destination_file_path)
            print(f"已复制 {cache_file_path} 到 {destination_file_path}")


def confirm(denoise, superres, filter_method, model, output_path, video_path, superres_scale, frame_rate):
    user_input_values = {
        'denoise': denoise,
        'superres': superres,
        'filter_method': filter_method,
        'model': model,
        'output_path': output_path,
        'video_path': video_path,
        'superres_scale': superres_scale,
        'frame_rate': frame_rate
    }
    print("Stored Values:", user_input_values)

    if not output_path or not video_path:
        print("Warning: File paths (video or output) aren't defined correctly.")
        return

    filter_function = {
        'Color blindness pattern': Color_blindness_pattern.filter,
        'Monochrome': Monochrome.filter,
        'Eye protection': Eye_protection.filter
    }.get(filter_method)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file at {video_path}.")
        return

    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        if filter_function:
            frame = filter_function(frame)
        frames.append(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()

    temp_dir = tempfile.mkdtemp()
    try:
        if denoise:
            ed.run_denoise(video_path, temp_dir)
            if not(model or superres):
                copy_files_from_cache_to_destination(temp_dir, output_path)
        if model:
            ed.run_film(temp_dir if denoise else video_path, temp_dir, frame_rate)
            if not superres:
                copy_files_from_cache_to_destination(temp_dir, output_path)
        if superres:
            final_output_path = generate_unique_path(output_path)
            ed.run_SuperResolution(temp_dir if model or denoise else video_path, final_output_path, superres_scale)
    finally:
        shutil.rmtree(temp_dir)

    print("Finish Process")


# run app
GUI.run_app(confirm)

