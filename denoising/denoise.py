import os.path
import logging
import argparse
import sys
import cv2
from models.network_dncnn import DnCNN as net
import numpy as np
from datetime import datetime
from collections import OrderedDict
# from scipy.io import loadmat

import torch

from utils import utils_logger
from utils import utils_model
from utils import utils_image as util


'''
Spyder (Python 3.6)
PyTorch 1.1.0
Windows 10 or Linux

Kai Zhang (cskaizhang@gmail.com)
github: https://github.com/cszn/KAIR
        https://github.com/cszn/DnCNN

@article{zhang2017beyond,
  title={Beyond a gaussian denoiser: Residual learning of deep cnn for image denoising},
  author={Zhang, Kai and Zuo, Wangmeng and Chen, Yunjin and Meng, Deyu and Zhang, Lei},
  journal={IEEE Transactions on Image Processing},
  volume={26},
  number={7},
  pages={3142--3155},
  year={2017},
  publisher={IEEE}
}

% If you have any question, please feel free to contact with me.
% Kai Zhang (e-mail: cskaizhang@gmail.com; github: https://github.com/cszn)

by Kai Zhang (12/Dec./2019)
'''

"""
# --------------------------------------------
|--model_zoo          # model_zoo
   |--dncnn_15        # model_name
   |--dncnn_25
   |--dncnn_50
   |--dncnn_gray_blind
   |--dncnn_color_blind
   |--dncnn3
|--testset            # testsets
   |--set12           # testset_name
   |--bsd68
   |--cbsd68
|--results            # results
   |--set12_dncnn_15  # result_name = testset_name + '_' + model_name
   |--set12_dncnn_25
   |--bsd68_dncnn_15
# --------------------------------------------
"""


def main(video_path, output_video_path):
    # ----------------------------------------
    # Argument Parsing
    # ----------------------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default='dncnn_color_blind',
                        help='dncnn_15, dncnn_25, dncnn_50, dncnn_gray_blind, dncnn_color_blind, dncnn3')
    parser.add_argument('--testset_name', type=str, default='img', help='test set, bsd68 | set12')
    parser.add_argument('--noise_level_img', type=int, default=50, help='noise level: 15, 25, 50')
    parser.add_argument('--x8', type=bool, default=False, help='x8 to boost performance')
    parser.add_argument('--show_img', type=bool, default=False, help='show the image')
    parser.add_argument('--model_pool', type=str, default='model_zoo', help='path of model_zoo')
    parser.add_argument('--results', type=str, default='results', help='path of results')
    parser.add_argument('--need_degradation', type=bool, default=False, help='add noise or not')
    parser.add_argument('--task_current', type=str, default='dn', help='dn for denoising')
    args = parser.parse_args()

    # Check if video_path exists
    if not os.path.exists(video_path):
        print(f"Video path {video_path} does not exist.")
        return

    # Create cache directories for frames
    cache_input_dir = os.path.join(video_path, "input_cache")
    cache_output_dir = os.path.join(video_path, "output_cache")
    os.makedirs(cache_input_dir, exist_ok=True)
    os.makedirs(cache_output_dir, exist_ok=True)

    # Device setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    n_channels = 3 if 'color' in args.model_name else 1
    nb = 20 if args.model_name in ['dncnn_gray_blind', 'dncnn_color_blind', 'dncnn3'] else 17
    model_path = os.path.join(args.model_pool, args.model_name + '.pth')

    # Load model
    model = net(in_nc=n_channels, out_nc=n_channels, nc=64, nb=nb, act_mode='BR')
    model.load_state_dict(torch.load(model_path), strict=True)
    model.eval().to(device)
    for _, param in model.named_parameters():
        param.requires_grad = False

    # Logger setup
    result_name = args.testset_name + '_' + args.model_name
    E_path = os.path.join(args.results, result_name)
    util.mkdir(E_path)
    logger_name = result_name
    utils_logger.logger_info(logger_name, log_path=os.path.join(E_path, logger_name + '.log'))
    logger = logging.getLogger(logger_name)

    # Extract frames from video_path and save to input_cache folder
    cap = cv2.VideoCapture(video_path)
    frame_idx = 0
    original_fps = cap.get(cv2.CAP_PROP_FPS)  # Get the original frame rate
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(cache_input_dir, f"frame_{frame_idx:04d}.png")
        cv2.imwrite(frame_path, frame)
        frame_idx += 1
    cap.release()

    # Process each frame in input_cache and save to output_cache
    for idx, frame_file in enumerate(sorted(os.listdir(cache_input_dir))):
        img_path = os.path.join(cache_input_dir, frame_file)
        img_L = util.imread_uint(img_path, n_channels=n_channels)
        img_L = util.uint2single(img_L)
        if args.need_degradation:  # degradation process
            np.random.seed(0)  # for reproducibility
            img_L += np.random.normal(0, args.noise_level_img / 255., img_L.shape)
        img_L = util.single2tensor4(img_L).to(device)

        # Denoising
        img_E = model(img_L) if not args.x8 else utils_model.test_mode(model, img_L, mode=3)
        img_E = util.tensor2uint(img_E)

        # Save processed frame to output_cache
        output_frame_path = os.path.join(cache_output_dir, frame_file)
        util.imsave(img_E, output_frame_path)

    # Convert processed frames from output_cache back to a video
    frame_paths = sorted([os.path.join(cache_output_dir, f) for f in os.listdir(cache_output_dir)])
    if len(frame_paths) == 0:
        print("No processed frames found in output_cache.")
        return

    # Get frame size
    sample_frame = cv2.imread(frame_paths[0])
    height, width, layers = sample_frame.shape
    video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), original_fps, (width, height))

    for frame_file in frame_paths:
        frame = cv2.imread(frame_file)
        video_writer.write(frame)

    video_writer.release()
    print(f"Processed video saved to {output_video_path}")


if __name__ == '__main__':
    video_path = sys.argv[1]
    output_video_path = sys.argv[2]
    main(video_path, output_video_path)
