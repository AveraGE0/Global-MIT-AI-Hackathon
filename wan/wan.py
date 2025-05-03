import torch
from diffusers import AutoencoderKLWan, WanPipeline
from diffusers.utils import export_to_video
import yaml

# Available models: Wan-AI/Wan2.1-T2V-14B-Diffusers, Wan-AI/Wan2.1-T2V-1.3B-Diffusers
model_id = "Wan-AI/Wan2.1-T2V-14B-Diffusers"
vae = AutoencoderKLWan.from_pretrained(model_id, subfolder="vae", torch_dtype=torch.float32)
pipe = WanPipeline.from_pretrained(model_id, vae=vae, torch_dtype=torch.bfloat16)
pipe.to("cuda")

with open("prompts.yaml", "r") as file:
    prompts = yaml.safe_load(file)

prompt = prompts["brainrot_1"]

negative_prompt = prompts["negative_2"]


output = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    height=832,
    width=480,
    num_frames=81,
    guidance_scale=3.0,
    num_videos_per_prompt=1
).frames[0]
export_to_video(output, "output/brainrot_1.mp4", fps=16)
