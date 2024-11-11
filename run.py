from GUI import GUI
import cv2
from filter import Monochrome, Eye_protection, Color_blindness_pattern
from film import frame_interpolation_UNet3D


# init dict
user_input_values = {}
# init test output path
test_output_path = 'output'


def confirm(denoise, superres, filter_method, model, output_path, video_path):
    user_input_values['denoise'] = denoise
    user_input_values['superres'] = superres
    user_input_values['filter_method'] = filter_method
    user_input_values['model'] = model
    user_input_values['output_path'] = output_path
    user_input_values['video_path'] = video_path

    # test print
    print("Stored Values:")
    print(user_input_values)

    # verify path
    if not user_input_values['output_path'] or not user_input_values['video_path']:
        print("Warning: File paths (video or output) aren't defined correctly.")
        return

    # set filter
    filter_function = None
    if user_input_values['filter_method'] == 'Color blindness pattern':
        filter_function = Color_blindness_pattern.filter
    elif user_input_values['filter_method'] == 'Monochrome':
        filter_function = Monochrome.filter
    elif user_input_values['filter_method'] == 'Eye protection':
        filter_function = Eye_protection.filter

    # open video
    cap = cv2.VideoCapture(user_input_values['video_path'])
    # error judge
    if not cap.isOpened():
        print(f"Error: Could not open video file at {user_input_values['video_path']}.")
        return

    frames = []  # store frame that after processing

    # frame process
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # use frame
        if filter_function:
            frame = filter_function(frame)

        # save changes
        frames.append(frame)

        # press 'q' to exit loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    # cv2.destroyAllWindows()

    # de-noise
    if user_input_values['denoise']:
        print("Applying de-noise...")

    # super resolution
    if user_input_values['superres']:
        print("Applying super-resolution...")

    # frame interpolation
    if user_input_values['model']:
        print(f"Applying model '{user_input_values['model']}'...")
        frame_interpolation_UNet3D(user_input_values['video_path'], user_input_values['output_path'], 60)

    # save video
    if user_input_values['output_path']:
        save_processed_video(frames, output_path)


def save_processed_video(frames, output_path, fps=30):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # set video encoder
    height, width, _ = frames[0].shape  # get frame size
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()
    print(f"Processed video saved to {output_path}.")


# run app
GUI.run_app(confirm)
