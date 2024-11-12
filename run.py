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


def confirm(denoise, superres, filter_method, model, output_path, video_path):
    user_input_values = {
        'denoise': denoise,
        'superres': superres,
        'filter_method': filter_method,
        'model': model,
        'output_path': output_path,
        'video_path': video_path
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
        if model:
            ed.run_film(temp_dir if denoise else video_path, temp_dir, 60)
        if superres:
            final_output_path = generate_unique_path(output_path)
            ed.run_SuperResolution(temp_dir if model or denoise else video_path, final_output_path)
    finally:
        shutil.rmtree(temp_dir)

    print("Finish Process")


# run app
GUI.run_app(confirm)

