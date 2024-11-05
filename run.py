from GUI import GUI
import cv2
from filter import Monochrome, Eye_protection, Color_blindness_pattern


user_input_values = {}  # init dict


def confirm(denoise, superres, filter_method, model, output_path, video_path):
    # store value into dict
    user_input_values['denoise'] = denoise  # bool
    user_input_values['superres'] = superres  # bool
    user_input_values['filter_method'] = filter_method  # string
    user_input_values['model'] = model  # string
    user_input_values['output_path'] = output_path  # string
    user_input_values['video_path'] = video_path  # string

    # print parameters
    print("Stored Values:")
    print(user_input_values)

    # 错误判定
    if output_path or video_path == '':
        print("Warning: File path isn't defined")

    # read video file
    cap = cv2.VideoCapture(user_input_values['video_path'])
    if not cap.isOpened():
        print("Error: Could not find the video file")
        exit()

    # frame operate
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # use filter
        if user_input_values['filter_method'] == 'Color blindness pattern':
            frame = Color_blindness_pattern.filter(frame)
        if user_input_values['filter_method'] == 'Monochrome':
            frame = Monochrome.filter(frame)
        if user_input_values['filter_method'] == 'Eye protection':
            frame = Eye_protection.filter(frame)

    cap.release()

    # use super-resolution

    # use model


GUI.run_app(confirm)