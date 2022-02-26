import cv2
from pathlib import Path
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, type=str, help="path to video")
ap.add_argument("-o", "--output", default="output", type=str, help="path for the images")

args = vars(ap.parse_args())

path = args['video']
output_dir = Path(args['output'])


max_scale = 1.0  # @param {type:'number'}
fps = 15  # @param {type:'number'}
target_num_frames = -1 # @param {type: 'number'}

cap = cv2.VideoCapture(path)
input_fps = cap.get(cv2.CAP_PROP_FPS)
num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

if num_frames < target_num_frames:
    raise RuntimeError(
        'The video is too short and has fewer frames than the target.')

if fps == -1:
    fps = int(target_num_frames / num_frames * input_fps)
    print(f"Auto-computed FPS = {fps}")

# @markdown Check this if you want to reprocess the frames.
overwrite = False  # @param {type:'boolean'}

if output_dir.exists() and not overwrite:
    raise RuntimeError(
        f'The RGB frames have already been processed. Check `overwrite` and run again if you really meant to do this.')
else:
    filters = f"mpdecimate,setpts=N/FRAME_RATE/TB,scale=iw*{max_scale}:ih*{max_scale}"
    tmp_rgb_raw_dir = 'rgb-raw'
    out_pattern = str('rgb-raw/%06d.png')
    !mkdir -p "$tmp_rgb_raw_dir"
    !ffmpeg -i "$video_path" -r $fps -vf $filters "$out_pattern"
    !mkdir -p "$rgb_raw_dir"
    !rsync -av "$tmp_rgb_raw_dir/" "$rgb_raw_dir/"