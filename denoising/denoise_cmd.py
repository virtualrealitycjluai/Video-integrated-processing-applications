import subprocess
import sys
import os


def run_inference(video_path, output_path):
    video_path = os.path.normpath(video_path)  # 统一路径分隔符
    output_path = os.path.normpath(output_path)
    cmd = [
        'python', 'denoise.py',
         video_path,
         output_path,
    ]

    try:
        # 使用 subprocess 调用外部脚本
        subprocess.run(cmd, check=True)
        print("处理完成！")
    except subprocess.CalledProcessError as e:
        print(f"发生错误：{e}")
    except Exception as e:
        print(f"未知错误：{e}")


print(sys.argv)
video_path = sys.argv[1]
output_video_path = sys.argv[2]


run_inference(video_path, output_video_path)
