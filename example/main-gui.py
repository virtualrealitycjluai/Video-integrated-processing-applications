# main_gui.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import sys
import os
import threading
import time


def run_task(env_path, script_path, task_name, log_file):
    """
    在指定的虚拟环境中运行指定的脚本，并显示日志内容。

    :param env_path: 虚拟环境的路径
    :param script_path: 要运行的脚本的路径
    :param task_name: 任务的名称，用于显示信息
    :param log_file: 日志文件的路径
    """
    # 确定Python解释器的路径
    if sys.platform == "win32":
        python_executable = os.path.join(env_path, "python.exe")
    else:
        python_executable = os.path.join(env_path, "bin", "python")

    # 检查Python解释器是否存在
    if not os.path.isfile(python_executable):
        messagebox.showerror("错误", f"找不到Python解释器：{python_executable}")
        return

    # 检查脚本文件是否存在
    if not os.path.isfile(script_path):
        messagebox.showerror("错误", f"找不到脚本文件：{script_path}")
        return

    try:
        # 启动子进程运行脚本
        subprocess.Popen([python_executable, script_path],
                         cwd=os.path.dirname(script_path),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        messagebox.showinfo("提示", f"{task_name} 已启动。")

        # 启动一个线程来监控日志文件
        threading.Thread(target=monitor_log, args=(log_file, task_name), daemon=True).start()
    except Exception as e:
        messagebox.showerror("执行错误", f"无法运行 {task_name}:\n{e}")


def monitor_log(log_file, task_name):
    """
    监控日志文件的变化，并将内容显示在GUI中。

    :param log_file: 日志文件的路径
    :param task_name: 任务的名称，用于显示信息
    """
    # 等待日志文件生成
    while not os.path.exists(log_file):
        time.sleep(0.5)

    with open(log_file, "r") as f:
        content = f.read()

    # 更新日志内容到文本区域
    output_text.configure(state='normal')
    output_text.insert(tk.END, f"--- {task_name} 输出 ---\n{content}\n")
    output_text.configure(state='disabled')


def run_task1():
    # 虚拟环境 env1 的路径
    env_path = r"D:\anaconda3\envs\en1"

    # task1.py 的完整路径
    script_path = r"E:\project_g3\deep learning\example\task1.py"

    # 日志文件路径
    log_file = os.path.join(os.path.dirname(script_path), "task1.log")

    run_task(env_path, script_path, "任务1", log_file)


def run_task2():
    # 虚拟环境 env2 的路径
    env_path = r"D:\anaconda3\envs\en2"

    # task2.py 的完整路径
    script_path = r"E:\project_g3\deep learning\example\task2.py"

    # 日志文件路径
    log_file = os.path.join(os.path.dirname(script_path), "task2.log")

    run_task(env_path, script_path, "任务2", log_file)


# 创建主窗口
root = tk.Tk()
root.title("多虚拟环境任务执行器")
root.geometry("600x400")

# 创建按钮
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

button1 = tk.Button(button_frame, text="运行任务1 (env1)", command=run_task1, width=20, height=2)
button1.grid(row=0, column=0, padx=10)

button2 = tk.Button(button_frame, text="运行任务2 (env2)", command=run_task2, width=20, height=2)
button2.grid(row=0, column=1, padx=10)

# 创建文本区域显示输出
output_text = scrolledtext.ScrolledText(root, state='disabled', width=70, height=15)
output_text.pack(pady=10)

# 运行主循环
root.mainloop()
