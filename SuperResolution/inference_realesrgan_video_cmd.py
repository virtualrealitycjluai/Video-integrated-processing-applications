import subprocess
import sys


def run_inference(video_path, output_path, superres_scale):
    # 构建命令行参数
    cmd = [
        'python', 'inference_realesrgan_video.py',
        '-i', video_path,  # 输入视频路径
        '-o', output_path,  # 输出路径
        '-s', superres_scale  # 超分辨率倍数
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
superres = sys.argv[3]
if superres in ['x2', 'x3', 'x4']:
    superres_new = (superres[1])
else:
    print("Invalid superres value. Using default x4 scale.")
    superres_new = '6'

run_inference(video_path, output_video_path, superres_new)