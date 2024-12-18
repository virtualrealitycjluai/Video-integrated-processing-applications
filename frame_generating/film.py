import cv2
import torch
import numpy as np
from torchvision import transforms
from model.VFIT_S import UNet_3D_3D
import sys
import os

print("Numpy version:", np.__version__)


def preprocess_frame(frame, device):
    frame_resized = cv2.resize(frame, (256, 256))
    transform = transforms.Compose([
        transforms.ToTensor(),
    ])
    frame_tensor = transform(frame_resized).unsqueeze(0).to(device)
    # frame_tensor = transform(frame).unsqueeze(0).to(device)
    return frame_tensor


def postprocess_frame(tensor):
    frame = tensor.squeeze(0).cpu().detach().numpy()
    frame = np.transpose(frame, (1, 2, 0))
    frame = np.clip(frame * 255.0, 0, 255).astype(np.uint8)
    return frame


def frame_interpolation_UNet3D(video_path, output_video_dir, aim_fps):
    output_video_path = os.path.join(output_video_dir, "_frame_generate_output.mp4")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # 加载模型
    model = UNet_3D_3D(n_inputs=4, joinType='concat')
    model = model.to(device)
    model.eval()

    checkpoint = torch.load('checkpoints/VFIT_S/model_best.pth', map_location=device)
    state_dict = checkpoint['state_dict']

    from collections import OrderedDict
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        if k.startswith('module.'):
            new_state_dict[k[7:]] = v
        else:
            new_state_dict[k] = v

    model.load_state_dict(new_state_dict)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        exit()
    else:
        print(f"Successfully opened video file: {video_path}")

    # 初始化帧缓冲区，读取前4帧
    frame_buffer = []
    for i in range(4):
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to read frame {i + 1}")
            cap.release()
            exit()
        frame_buffer.append(frame)
        print(f"Successfully read frame {i + 1}, shape: {frame.shape}")

    # 获取视频属性
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("FPS not found, using default 30 FPS")
        fps = 30  # 默认帧率
    else:
        print(f"Video FPS: {fps}")

    frame_height, frame_width, _ = frame_buffer[0].shape

    # 初始化视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, aim_fps, (frame_width, frame_height))
    if out.isOpened():
        print(f"Successfully opened video writer for output: {output_video_path}")
    else:
        print(f"Failed to open video writer for output: {output_video_path}")
        exit()

    while True:
        # 预处理帧，inputs 是一个张量列表
        inputs = [preprocess_frame(frame, device) for frame in frame_buffer]

        with torch.no_grad():
            # 模型推理，直接传入帧列表
            output = model(inputs)

        # 后处理输出
        interpolated_frame = postprocess_frame(output)

        # 调整大小以显示
        interpolated_frame_resized = cv2.resize(interpolated_frame,
                                                (frame_buffer[1].shape[1], frame_buffer[1].shape[0]))

        # 将原始帧和插值帧写入视频
        out.write(frame_buffer[1])  # 写入当前帧
        print(f"Written frame {len(frame_buffer)} to output.")

        out.write(interpolated_frame_resized)  # 写入插值帧
        print(f"Written interpolated frame to output.")

        # 读取下一帧并更新帧缓冲区
        ret, next_frame = cap.read()
        if not ret:
            # 如果没有更多帧，写入剩余帧
            out.write(frame_buffer[2])  # 写入最后一帧
            break  # 视频结束

        frame_buffer.pop(0)
        frame_buffer.append(next_frame)

    # 释放资源
    cap.release()
    out.release()
    print(f"Video interpolation completed and saved to {output_video_path}")


if __name__ == "__main__":
    video_path = sys.argv[1]
    output_video_path = sys.argv[2]
    aim_fps = int(sys.argv[3])
    print(sys.argv)
    frame_interpolation_UNet3D(video_path, output_video_path, aim_fps)