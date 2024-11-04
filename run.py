from GUI import GUI

user_input_values = {}  # init dict


def confirm(denoise, superres, filter_method, model, output_path, video_path):
    # store value into dict
    user_input_values['denoise'] = denoise
    user_input_values['superres'] = superres
    user_input_values['filter_method'] = filter_method
    user_input_values['model'] = model
    user_input_values['output_path'] = output_path
    user_input_values['video_path'] = video_path

    # print
    print("Stored Values:")
    print(user_input_values)


GUI.run_app(confirm)