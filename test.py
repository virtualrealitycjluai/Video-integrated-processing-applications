import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import sys
import os
import threading
import queue

# 配置路径
env_path = r"E:\projectDeeplearning\environment\myenv"
task_name = "测试任务"
script_path = r"E:\projectDeeplearning\frame_generating.py"

# 根据系统平台设置Python解释器路径
if sys.platform == "win32":
    python_executable = os.path.join(env_path, "python.exe")
else:
    python_executable = os.path.join(env_path, "bin", "python")

# 定义输入和输出视频路径（使用默认值）
input_video_path = r"E:\projectDeeplearning\video\4.mp4"
output_video_path = r"E:\projectDeeplearning\output\output_video.mp4"

# 创建主窗口
root = tk.Tk()
root.title("视频帧插值工具")
root.geometry("800x600")  # 调整窗口大小以适应更多输出

# 创建一个队列用于线程间通信
q = queue.Queue()

# 全局变量用于管理子进程
process = None

# 输出到ScrolledText控件的函数
def display_output(pipe, queue):
    for line in iter(pipe.readline, ''):
        queue.put(line)
    pipe.close()

# 子进程结束时的回调函数
def on_process_complete(process):
    process.wait()  # 确保子进程已完全结束
    if process.returncode == 0:
        q.put(f"{task_name} 运行完成。\n")
    else:
        q.put(f"{task_name} 运行出错，错误码：{process.returncode}\n")

# 轮询队列并更新GUI
def poll_queue():
    while not q.empty():
        line = q.get()
        output_text.config(state='normal')
        output_text.insert(tk.END, line)
        output_text.yview(tk.END)  # 自动滚动到底部
        output_text.config(state='disabled')
    root.after(100, poll_queue)  # 每100毫秒检查一次队列

# 运行任务的函数
def run_task():
    global process
    try:
        # 检查输入视频文件是否存在
        if not os.path.exists(input_video_path):
            messagebox.showerror("错误", f"输入视频文件未找到：{input_video_path}")
            return

        # 检查脚本文件是否存在
        if not os.path.exists(script_path):
            messagebox.showerror("错误", f"脚本文件未找到：{script_path}")
            return

        # 清空之前的输出
        output_text.config(state='normal')
        output_text.delete(1.0, tk.END)
        output_text.config(state='disabled')

        # 启动子进程
        process = subprocess.Popen(
            [python_executable, script_path],
            cwd=os.path.dirname(script_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,  # 行缓冲
            universal_newlines=True  # 以文本模式读取
        )
        q.put(f"{task_name} 已启动。\n")

        # 创建线程来显示标准输出和错误输出
        threading.Thread(target=display_output, args=(process.stdout, q), daemon=True).start()
        threading.Thread(target=display_output, args=(process.stderr, q), daemon=True).start()

        # 创建线程监控子进程结束
        threading.Thread(target=on_process_complete, args=(process,), daemon=True).start()

    except Exception as e:
        messagebox.showerror("错误", f"启动任务失败：{str(e)}")

# 停止任务的函数
def stop_task():
    try:
        global process
        if process and process.poll() is None:
            process.terminate()
            q.put(f"{task_name} 已被终止。\n")
    except Exception as e:
        messagebox.showerror("错误", f"停止任务失败：{str(e)}")

# 创建按钮框架
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# 创建运行任务按钮
run_button = tk.Button(button_frame, text="运行帧插值任务", command=run_task, width=20, height=2, bg='green', fg='white')
run_button.grid(row=0, column=0, padx=10)

# 创建停止任务按钮
stop_button = tk.Button(button_frame, text="停止任务", command=stop_task, width=20, height=2, bg='red', fg='white')
stop_button.grid(row=0, column=1, padx=10)

# 创建文本区域显示输出
output_text = scrolledtext.ScrolledText(root, state='disabled', width=100, height=30, font=("Consolas", 10))
output_text.pack(pady=10, padx=10)

# 启动轮询队列
root.after(100, poll_queue)

# 运行主循环
root.mainloop()
