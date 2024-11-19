import subprocess
import sys
import os


def run_inference(video_path, output_path):
    video_path = os.path.normpath(video_path)  # 统一路径分隔符
    output_path = os.path.normpath(output_path)
    cmd = [
        'python', 'denoise.py',
        '--video_path', video_path,  # 假设这是视频路径的参数
        '--results', output_path  # 假设这是输出路径的参数
    ]

    print(f"准备执行命令: {cmd}")  # 输出要执行的命令

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("处理完成！")
        print("标准输出:", result.stdout)
        print("标准错误:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"发生错误：{e}")
        print("错误标准输出:", e.stdout)
        print("错误标准错误:", e.stderr)
    except Exception as e:
        print(f"未知错误：{e}")

    try:
        # 使用 subprocess 调用外部脚本
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("处理完成！")
        print("标准输出", result.stdout)
        print("标准错误", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"发生错误：{e}")
        print("标准输出:", e.stdout)
        print("标准错误:", e.stderr)
    except Exception as e:
        print(f"未知错误：{e}")


print(sys.argv)
video_path = sys.argv[1]
output_video_path = sys.argv[2]

run_inference(video_path, output_video_path)
