from GUI import GUI
import cv2
from filter import Monochrome, Eye_protection, Color_blindness_pattern
from env_bridge import env_distribute as ed
import os
import shutil


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


def clear_temp_folder(folder):
    """
    清空指定文件夹中的所有文件和子文件夹，但不删除文件夹本身。
    """
    if os.path.exists(folder):
        for root, dirs, files in os.walk(folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))  # 删除文件
            for name in dirs:
                os.rmdir(os.path.join(root, name))  # 删除空的子文件夹
        print(f"已清空文件夹 {folder} 中的所有文件和子文件夹")
    else:
        print(f"文件夹 {folder} 不存在")


temp1 = "temp1"
temp2 = "temp2"


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

    if denoise:
        ed.run_denoise(video_path, temp1)
        if not(model or superres):
            copy_files_from_cache_to_destination(temp1, output_path)
    if model:
        temp2_path = os.path.abspath('temp2')
        ed.run_film(temp1 if denoise else video_path, temp2_path, frame_rate)
        if not superres:
            copy_files_from_cache_to_destination(temp2, output_path)
    if superres:
        temp2_path = os.path.abspath('temp2')
        ed.run_SuperResolution(temp2 if model or denoise else video_path, output_path, superres_scale)

    print("Finish Process")

    # clear_temp_folder(temp1)
    # clear_temp_folder(temp2)


# run app
GUI.run_app(confirm)

