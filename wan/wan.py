import torch
from diffusers import AutoencoderKLWan, WanPipeline
from diffusers.utils import export_to_video
import yaml
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description="Process video generation parameters.")
parser.add_argument("--small_model", action="store_true")
parser.add_argument("--prompt_id", type=int, default=1, help="Which prompt from the .yaml to pick")
parser.add_argument("--negative_prompt_id", type=int, default=1, help="Path to the output video.")
parser.add_argument("--output_name", type=str, default=datetime.now().strftime("%Y%m%d_%H%M%S"))
parser.add_argument("--video_duration", type=int, default=5)

args = parser.parse_args()

small_model = args.small_model
prompt_id = args.prompt_id
negative_prompt_id = args.negative_prompt_id
output_name = args.output_name
duration = args.video_duration

# Available models: Wan-AI/Wan2.1-T2V-14B-Diffusers, Wan-AI/Wan2.1-T2V-1.3B-Diffusers
model_id = "Wan-AI/Wan2.1-T2V-14B-Diffusers" if not small_model else "Wan-AI/Wan2.1-T2V-1.3B-Diffusers"
vae = AutoencoderKLWan.from_pretrained(model_id, subfolder="vae", torch_dtype=torch.float32)
pipe = WanPipeline.from_pretrained(model_id, vae=vae, torch_dtype=torch.bfloat16)
pipe.to("cuda")

with open("prompts.yaml", "r") as file:
    prompts = yaml.safe_load(file)

prompt = prompts[f"prompt_{prompt_id}"]

negative_prompt = prompts[f"negative_prompt_{negative_prompt_id}"]

fps=16
num_frames = (duration * fps) + 1

output = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    height=832,
    width=480,
    num_frames=num_frames,
    guidance_scale=3.0,
    num_videos_per_prompt=1
).frames[0]
export_to_video(output, f"output/{output_name}.mp4", fps=fps)
