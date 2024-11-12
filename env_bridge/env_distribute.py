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
    # 确定Python解释器的路径
    if sys.platform == "win32":
        python_executable = os.path.join(env_path, "python.exe")
    else:
        python_executable = os.path.join(env_path, "bin", "python")

    # 检查Python解释器是否存在
    if not os.path.isfile(python_executable):
        print(f"错误: 找不到Python解释器：{python_executable}")
        return

    # 检查脚本文件是否存在
    if not os.path.isfile(script_path):
        print(f"错误: 找不到脚本文件：{script_path}")
        return

    try:
        # 启动子进程运行脚本并传递参数
        subprocess.Popen(
            [python_executable, script_path, video_path, output_video_path, str(aim_fps)],
            cwd=os.path.dirname(script_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"提示: {task_name} 已启动。")

        # 启动一个线程来监控日志文件
        threading.Thread(target=monitor_log, args=(log_file, task_name), daemon=True).start()
    except Exception as e:
        print(f"执行错误: 无法运行 {task_name}:\n{e}")


def run_SuperResolution_task(env_path, script_path, task_name, log_file, video_path, output_video_path):
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

    try:
        subprocess.Popen(
            [python_executable, script_path, video_path, output_video_path],
            cwd=os.path.dirname(script_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
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

    try:
        subprocess.Popen(
            [python_executable, script_path, video_path, output_video_path],
            cwd=os.path.dirname(script_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
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
    # 等待日志文件生成
    while not os.path.exists(log_file):
        time.sleep(0.5)

    with open(log_file, "r") as f:
        content = f.read()

    # 打印日志内容到控制台
    print(f"--- {task_name} 输出 ---\n{content}\n")


def run_film(video_path=r'E:\projectDeeplearning\video\4.mp4',
             output_video_path=r'E:\projectDeeplearning\output\output_video.mp4', aim_fps=60):
    # 指定虚拟环境路径
    env_path = r"E:\projectDeeplearning\environment\dl"
    # 要执行的脚本
    script_path = r"E:\projectDeeplearning\env_bridge\film.py"
    log_file = os.path.join(os.path.dirname(script_path), "film.log")
    run_film_task(env_path, script_path, "film", log_file, video_path, output_video_path, aim_fps)


def run_SuperResolution(video_path=r'E:\projectDeeplearning\video\4.mp4',
                        output_video_path=r'E:\projectDeeplearning\output\output_video.mp4'):
    env_path = r""
    script_path = r"SuperResolution\inference_realesrgan_video.py"
    log_file = os.path.join(os.path.dirname(script_path), "SuperResolution.log")
    run_SuperResolution_task(env_path, script_path, "SuperResolution", log_file, video_path, output_video_path)


def run_denoise(video_path=r'E:\projectDeeplearning\video\4.mp4',
                output_video_path=r'E:\projectDeeplearning\output\output_video.mp4'):
    env_path = r""
    script_path = r"E:\projectDeeplearning\env_bridge\denoise.py"
    log_file = os.path.join(os.path.dirname(script_path), "denoise.log")
    run_denoise_task(env_path, script_path, "denoise", log_file, video_path, output_video_path)
