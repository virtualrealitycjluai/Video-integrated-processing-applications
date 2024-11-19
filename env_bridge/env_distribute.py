import subprocess
import sys
import os
import threading
import time


def run_film_task(env_path, script_path, task_name, log_file, video_path, output_video_path, aim_fps):
    """
    在指定的虚拟环境中运行指定的脚本，并显示日志内容。

    :param env_path: 虚拟环境的路径
    :param script_path: 要运行的脚本的路径
    :param task_name: 任务的名称，用于显示信息
    :param log_file: 日志文件的路径
    :param video_path: 输入视频的路径
    :param output_video_path: 输出视频的路径
    :param aim_fps: 目标帧率
    """
    if sys.platform == "win32":
        python_executable = os.path.join(env_path, "python.exe")
    else:
        python_executable = os.path.join(env_path, "bin", "python")

    if not os.path.isfile(python_executable):
        print(f"错误: 找不到Python解释器：{python_executable}")
        return

    if not os.path.isfile(script_path):
        print(f"错误: 找不到脚本文件：{script_path}")
        return
    env = os.path.basename(env_path)
    command = f'conda activate {env} && {python_executable} {script_path} {video_path} {output_video_path} {aim_fps}'
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(script_path)
        )
        # 获取标准输出和错误输出
        stdout, stderr = process.communicate()

        # 打印输出和错误信息
        print("Standard Output:\n", stdout.decode())
        print("Standard Error:\n", stderr.decode())
        print(os.path.dirname(script_path))
        print(f"提示: {task_name} 已启动。")
        threading.Thread(target=monitor_log, args=(log_file, task_name), daemon=True).start()
    except Exception as e:
        print(f"执行错误: 无法运行 {task_name}:\n{e}")


def run_SuperResolution_task(env_path, script_path, task_name, log_file, video_path, output_video_path, superres_scale):
    if sys.platform == "win32":
        python_executable = os.path.join(env_path, "python.exe")
    else:
        python_executable = os.path.join(env_path, "bin", "python")

    if not os.path.isfile(python_executable):
        print(f"错误: 找不到Python解释器：{python_executable}")
        return

    if not os.path.isfile(script_path):
        print(f"错误: 找不到脚本文件：{script_path}")
        return
    env = os.path.basename(env_path)
    command = f'conda activate {env} && {python_executable} {script_path} {video_path} {output_video_path} {superres_scale}'
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(script_path)
        )
        stdout, stderr = process.communicate()

        print("Standard Output:\n", stdout.decode())
        print("Standard Error:\n", stderr.decode())
        print(os.path.dirname(script_path))
        print(f"提示: {task_name} 已启动。")
        threading.Thread(target=monitor_log, args=(log_file, task_name), daemon=True).start()
    except Exception as e:
        print(f"执行错误: 无法运行 {task_name}:\n{e}")


def run_denoise_task(env_path, script_path, task_name, log_file, video_path, output_video_path):
    if sys.platform == "win32":
        python_executable = os.path.join(env_path, "python.exe")
    else:
        python_executable = os.path.join(env_path, "bin", "python")

    if not os.path.isfile(python_executable):
        print(f"错误: 找不到Python解释器：{python_executable}")
        return

    if not os.path.isfile(script_path):
        print(f"错误: 找不到脚本文件：{script_path}")
        return
    env = os.path.basename(env_path)
    command = f'conda activate {env} && {python_executable} {script_path} {video_path} {output_video_path}'
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(script_path)
        )
        stdout, stderr = process.communicate()

        print("Standard Output:\n", stdout.decode())
        print("Standard Error:\n", stderr.decode())
        print(os.path.dirname(script_path))
        print(f"提示: {task_name} 已启动。")
        threading.Thread(target=monitor_log, args=(log_file, task_name), daemon=True).start()
    except Exception as e:
        print(f"执行错误: 无法运行 {task_name}:\n{e}")


def monitor_log(log_file, task_name):
    """
    监控日志文件的变化，并将内容打印到控制台。

    :param log_file: 日志文件的路径
    :param task_name: 任务的名称，用于显示信息
    """
    while not os.path.exists(log_file):
        time.sleep(0.5)

    with open(log_file, "r") as f:
        content = f.read()

    print(f"--- {task_name} 输出 ---\n{content}\n")


# 设定环境路径和脚本路径
# env_path = r"E:\projectDeeplearning\environment\dl"
env_path_film = r"E:\anaconda3\envs\lcr"
env_path_super_resolution = r"E:\anaconda3\envs\lcr"
env_path_denoisy = r"E:\anaconda3\envs\lcr"
script_path_film = r"E:\projectDeeplearning\frame_generating\film.py"
script_path_denoise = r"E:\projectDeeplearning\denoising\denoise_cmd.py"
script_path_superres = r"E:\projectDeeplearning\SuperResolution\inference_realesrgan_video_cmd.py"

# 日志文件路径
log_file_film = os.path.join(os.path.dirname("logs/film.log"), "film.log")
log_file_denoise = os.path.join(os.path.dirname("logs/denoise.log"), "denoise.log")
log_file_superres = os.path.join(os.path.dirname("logs/SuperResolution.log"), "SuperResolution.log")


def run_film(video_path, output_video_path, aim_fps):
    run_film_task(env_path_film, script_path_film,
                  "film", log_file_film, video_path, output_video_path, aim_fps)


def run_SuperResolution(video_path, output_video_path, superres_scale):
    run_SuperResolution_task(env_path_super_resolution, script_path_superres,
                             "SuperResolution", log_file_superres, video_path, output_video_path, superres_scale)


def run_denoise(video_path, output_video_path):
    run_denoise_task(env_path_denoisy, script_path_denoise,
                     "denoise", log_file_denoise, video_path, output_video_path)
